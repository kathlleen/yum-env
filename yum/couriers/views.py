import os
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from orders.models import Order
import json
from django.http import JsonResponse
from django.utils import timezone
from common.mixins import CacheMixin
from couriers.forms import CourierProfileForm


def is_courier(user):
    return user.is_authenticated and user.is_courier()

@login_required
@user_passes_test(is_courier, login_url='main:index')
def courier_dashboard(request):
    courier = request.user

    if not courier:
        return redirect('main:index')

    # Получаем заказы для курьера
    orders = Order.objects.filter(courier=courier).order_by('-id')
    process_orders = orders.filter(status='processing')
    wait_orders = orders.filter(status='awaiting_delivery')
    active_orders = orders.filter(status='on_the_way')

    context = {
        'title': 'Панель курьера',
        'process_orders': process_orders,
        'wait_orders': wait_orders,
        'active_orders': active_orders,
    }

    return render(request, 'couriers/courier_dashboard.html', context)

class CourierProfileView(LoginRequiredMixin, CacheMixin, UpdateView):
    template_name = 'couriers/courier_profile.html'
    form_class = CourierProfileForm
    success_url = reverse_lazy('couriers:courier-profile')

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
        return context


@login_required
@user_passes_test(is_courier, login_url='main:index')
def courier_statistics(request):
    context = {
        'title': 'Статистика курьера'
    }
    return render(request, 'couriers/courier_statistics.html', context)

@login_required
@user_passes_test(is_courier, login_url='main:index')
def toggle_shift(request):
    user = request.user
    user.on_shift = not user.on_shift
    user.save()
    return redirect('couriers:courier-dashboard')


@csrf_exempt
def update_location(request):
    if request.method == 'POST' and request.user.is_authenticated and request.user.is_courier():
        data = json.loads(request.body)
        lat = data.get('latitude')
        lon = data.get('longitude')

        if lat is not None and lon is not None and request.user.on_shift:
            request.user.latitude = lat
            request.user.longitude = lon
            request.user.last_location_update = timezone.now()
            request.user.save()
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'error', 'message': 'Invalid data or not on shift'}, status=400)

    return JsonResponse({'status': 'unauthorized'}, status=401)