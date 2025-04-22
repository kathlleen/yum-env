from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from orders.models import Order

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

@login_required
@user_passes_test(is_courier, login_url='main:index')
def courier_profile(request):
    context = {
        'title': 'Профиль курьера'
    }
    return render(request, 'couriers/courier_profile.html', context)


@login_required
@user_passes_test(is_courier, login_url='main:index')
def courier_statistics(request):
    context = {
        'title': 'Статистика курьера'
    }
    return render(request, 'couriers/courier_statistics.html', context)