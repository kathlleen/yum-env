import os
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from orders.models import Order
import json
from django.http import JsonResponse
from django.utils import timezone
from common.mixins import CacheMixin
from couriers.forms import CourierProfileForm

from orders.models import OrderRating

from couriers.models import Shift


def is_courier(user):
    return user.is_authenticated and user.is_courier()

@login_required
@user_passes_test(is_courier, login_url='main:index')
def courier_dashboard(request):
    courier = request.user
    active_shift = Shift.objects.filter(courier=courier, end_time__isnull=True).last()

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
        'active_shift': active_shift,
    }

    return render(request, 'couriers/courier_dashboard.html', context)


@login_required
def mark_order_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id, courier=request.user)

    if request.method == 'POST':
        order.status = 'delivered'
        order.save()

    return redirect('couriers:courier-dashboard')  # Или куда надо

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
    courier = request.user
    now = timezone.now()

    # Временные промежутки
    today = now.date()
    start_week = today - timedelta(days=today.weekday())  # понедельник
    start_month = today.replace(day=1)

    # Все доставленные заказы
    delivered_orders = Order.objects.filter(courier=courier, status='delivered')

    # Фильтры по времени
    today_orders = delivered_orders.filter(created_timestamp__date=today)
    week_orders = delivered_orders.filter(created_timestamp__date__gte=start_week)
    month_orders = delivered_orders.filter(created_timestamp__date__gte=start_month)

    # Деньги (предположим 5% получает курьер)
    COMMISSION_COURIER = Decimal('0.05')
    COMMISSION_SERVICE = Decimal('0.10')

    def calc_total_earned(orders):
        total = Decimal('0.00')
        for order in orders:
            items = order.orderitem_set.all()
            order_sum = sum(item.price * item.quantity for item in items)
            total += order_sum * COMMISSION_COURIER
        return total.quantize(Decimal('0.01'))

    def get_avg_rating(model_queryset, field_name):
        ratings = model_queryset.values_list(field_name, flat=True)[:100]
        if not ratings:
            return None
        return round(sum(ratings) / len(ratings), 2)

    shifts = courier.shifts.all()
    total_shift_time = timedelta()

    for shift in shifts:
        if shift.end_time:
            total_shift_time += shift.end_time - shift.start_time
        else:
            total_shift_time += timezone.now() - shift.start_time

    # Рейтинг
    ratings = OrderRating.objects.filter(courier=courier).order_by('-created_at')
    avg_rating = get_avg_rating(ratings, 'courier_rating')

    context = {
        'title': 'Статистика курьера',
        'orders_today': today_orders.count(),
        'orders_week': week_orders.count(),
        'orders_month': month_orders.count(),
        'earned_today': calc_total_earned(today_orders),
        'earned_week': calc_total_earned(week_orders),
        'earned_month': calc_total_earned(month_orders),
        'avg_rating': avg_rating,
        'total_shift_time': total_shift_time,  # timedelta
        'days_worked_week': week_orders.values('created_timestamp__date').distinct().count(),
        'days_worked_month': month_orders.values('created_timestamp__date').distinct().count(),
    }

    return render(request, 'couriers/courier_statistics.html', context)

@login_required
@user_passes_test(is_courier, login_url='main:index')
def toggle_shift(request):
    user = request.user
    if user.on_shift:
        # Завершение смены
        user.on_shift = False
        shift = Shift.objects.filter(courier=user, end_time__isnull=True).last()
        if shift:
            shift.end_time = timezone.now()
            shift.save()
    else:
        # Начало новой смены
        user.on_shift = True
        Shift.objects.create(courier=user)

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