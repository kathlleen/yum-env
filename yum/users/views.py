from django.contrib import auth
from django.contrib.auth import authenticate,  login as auth_login
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from users.forms import UserLoginForm, CustomerRegistrationForm, \
    RestaurantAdminRegistrationForm,CourierRegistrationForm, ProfileForm
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
# from users.models import CustomUser

from carts.models import Cart
from common.mixins import CacheMixin
from orders.models import Order, OrderItem
from django.db.models import Prefetch

import os
from django.conf import settings

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
        context['profile'] = True
        context['orders'] = self.set_get_cache(orders, f"user_{self.request.user.id}_orders", 60 * 2)
        return context


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
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))