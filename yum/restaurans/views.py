from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Order

@login_required
def restaurant_dashboard(request):
    # Проверяем, что пользователь связан с рестораном
    restaurant = request.user.restaurant

    if not restaurant:
        return redirect('main:index')  # Перенаправляем, если у пользователя нет ресторана

    # Получаем заказы для ресторана
    orders = Order.objects.filter(restaurant=restaurant)

    context = {
        'title': f'{restaurant.name} Админ',
        'restaurant': restaurant,
        'orders': orders,  # Передаем заказы в шаблон
    }

    return render(request, 'restaurans/restaurant_dashboard.html', context)
