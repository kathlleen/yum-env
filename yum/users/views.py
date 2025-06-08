from django.contrib import auth
from django.contrib.auth import authenticate,  login as auth_login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView
from users.forms import UserLoginForm, CustomerRegistrationForm, \
    RestaurantAdminRegistrationForm,CourierRegistrationForm, ProfileForm
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
# from users.models import CustomUser

from carts.models import Cart
from common.mixins import CacheMixin
from orders.models import Order, OrderItem
from django.db.models import Prefetch, Avg

import os
from django.conf import settings

from menu.models import LabelPreference
from users.forms import UserPreferenceForm

from orders.models import OrderRating
from django.core.cache import cache

# Create your views here.
class UserLoginView(FormView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_success_url(self):
        # If there's a next parameter in the POST request, use that for redirection
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index')

    def form_valid(self, form):
        # Form is valid, so proceed with user authentication and session management
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        session_key = self.request.session.session_key

        if user:
            auth_login(self.request, user)

            if user.is_restaurant_admin():
                # If the user is a restaurant admin, redirect to restaurant dashboard
                return HttpResponseRedirect(reverse('restaurans:restaurant-dashboard'))

            if user.is_courier():
                return HttpResponseRedirect(reverse('couriers:courier-dashboard'))

            if session_key:
                # If the user was not previously logged in, update any cart items
                Cart.objects.filter(session_key=session_key).update(user=user)

            return HttpResponseRedirect(self.get_success_url())

        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Authorization'
        return context

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

        # Исключаем уже оценённые
        rated_order_ids = OrderRating.objects.filter(
            order__customer=self.request.user
        ).values_list('order_id', flat=True)

        orders = Order.objects.filter(
            customer=self.request.user
        ).exclude(
            id__in=rated_order_ids
        ).prefetch_related(
            Prefetch("orderitem_set", queryset=OrderItem.objects.select_related("dish"))
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
        context['profile'] = True
        context['orders'] = orders
        return context

@require_POST
@login_required
def rate_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user, status='delivered')

    # Не даём оценивать повторно
    if OrderRating.objects.filter(order=order).exists():
        return redirect('users:profile')

    try:
        courier_rating = int(request.POST.get('courier_rating', 0))
        restaurant_rating = int(request.POST.get('restaurant_rating', 0))
    except (ValueError, TypeError):
        print("ОШИБКА С ОЦЕНКОЙ!!")
        return redirect('users:profile')  # Или верни ошибку / сообщение

    # Создаём оценку
    OrderRating.objects.create(
        order=order,
        courier=order.courier,
        restaurant=order.restaurant,
        courier_rating=courier_rating,
        restaurant_rating=restaurant_rating
    )

    # ⏱ Пересчёт рейтинга ресторана (за последний месяц)
    start_of_month = timezone.now().replace(day=1)

    avg_rating = OrderRating.objects.filter(
        restaurant=order.restaurant,
        created_at__date__gte=start_of_month
    ).aggregate(avg=Avg('restaurant_rating'))['avg']

    order.restaurant.rating = round(avg_rating or 0, 1)
    order.restaurant.save(update_fields=['rating'])

    return redirect('users:profile')


class CustomerRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        session_key = self.request.session.session_key
        user = form.save()

        if user:
            auth_login(self.request, user)

        if session_key:
            Cart.objects.filter(session_key=session_key).update(user=user)

        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['url'] = 'users:register_customer'
        return context

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class RestaurantAdminRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = RestaurantAdminRegistrationForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = 'restaurant_admin'  # Set the user type
        user.save()
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация администратора ресторана'
        context['url'] = 'users:register_restaurant_admin'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CourierRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = CourierRegistrationForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация курьера'
        context['url'] = 'users:register_courier'
        return context

@login_required
def preferences_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=user, user=user)
        if form.is_valid():
            form.save()

            # Удалим старые предпочтения
            LabelPreference.objects.filter(user=user).delete()

            # Сохраняем новые
            for pref_type in ['like', 'dislike', 'diet', 'allergy']:
                labels = form.cleaned_data.get(f'{pref_type}_labels')
                for label in labels:
                    LabelPreference.objects.create(
                        user=user,
                        label=label,
                        preference_type=pref_type
                    )
            return redirect('users:profile')  # или куда нужно
    else:
        form = UserPreferenceForm(user=user, instance=user)

    return render(request, 'users/preferences.html', {'form': form})

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))