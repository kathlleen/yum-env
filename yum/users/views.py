from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from users.forms import UserLoginForm, CustomerRegistrationForm, \
    RestaurantAdminRegistrationForm,CourierRegistrationForm, ProfileForm
# from users.models import CustomUser

from carts.models import Cart
from common.mixins import CacheMixin
from orders.models import Order, OrderItem
from django.db.models import Prefetch

import os
from django.conf import settings

# Create your views here.
def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)

                if user.is_restaurant_admin():
                    restaurant = user.restaurant  # Получаем ресторан, которым управляет админ
                    return render(request, 'restaurans/restaurant_dashboard.html', {'restaurant': restaurant})

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                return HttpResponseRedirect(reverse('main:index'))

    else:
        form = UserLoginForm()

    context = {
        'title' : "Authorization",
        'form': form,
    }
    return render(request, 'users/login.html',context)


class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        selected_avatar = self.request.POST.get('selected_avatar')

        if selected_avatar:
            # Сохраняем выбранный аватар
            self.request.user.image = selected_avatar

        # Обрабатываем загруженное изображение (если есть)
        if self.request.FILES.get('image'):
            self.request.user.image = self.request.FILES['image']

        self.request.user.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile'

        orders = Order.objects.filter(customer=self.request.user).prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("dish"),
            )
        ).order_by("-id")

        # Получаем список изображений из папки media/avatars/
        avatar_directory = os.path.join(settings.MEDIA_ROOT, 'avatars')
        avatar_files = []

        # Проверяем наличие папки и собираем список файлов
        if os.path.exists(avatar_directory):
            # Преобразуем пути в правильный формат
            avatar_files = [os.path.join('avatars', f).replace("\\", "/") for f in os.listdir(avatar_directory) if
                            f.endswith(('jpg', 'jpeg', 'png', 'webp'))]

        context['avatar_files'] = avatar_files
        context['MEDIA_URL'] = settings.MEDIA_URL

        context['orders'] = self.set_get_cache(orders, f"user_{self.request.user.id}_orders", 60 * 2)
        return context


def register_customer(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = CustomerRegistrationForm()


    context = {
        'title' : "Регистрация",
        'form' : form,
        'url': 'users:register_customer'
    }
    return render(request, 'users/registration.html',context)


@user_passes_test(lambda u: u.is_superuser)
def register_restaurant_admin(request):
    if request.method == 'POST':
        form = RestaurantAdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Устанавливаем тип пользователя как администратор ресторана
            user.user_type = 'restaurant_admin'
            user.save()
        return HttpResponseRedirect(reverse('main:index'))
    else:
        form = RestaurantAdminRegistrationForm()

    context = {
        'title': "Регистрация администратора ресторана",
        'form': form,
        'url' : 'users:register_restaurant_admin'
    }
    return render(request, 'users/registration.html', context)




@user_passes_test(lambda u: u.is_superuser)
def register_courier(request):
    if request.method == 'POST':
        form = CourierRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = CourierRegistrationForm()

    context = {
        'title': "Регистрация курьера",
        'form': form,
        'url': 'users:register_courier'
    }
    return render(request, 'users/registration.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))