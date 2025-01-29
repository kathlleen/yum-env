from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from orders.models import Order

from django.views.generic.edit import FormView
from menu.models import Dish

from users.forms import RestProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from common.mixins import CacheMixin


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

@login_required
def restaurant_edit(request):
    restaurant = request.user.restaurant

    dishes = Dish.objects.filter(restaurant=restaurant)

    if not restaurant:
        return redirect('main:index')

    context = {
        'title': f'{restaurant.name} Редактирование',
        'restaurant': restaurant,
        'dishes': dishes,  # Передаем заказы в шаблон
    }

    return render(request, 'restaurans/restaurant_edit.html', context)



class RestEditView(LoginRequiredMixin, UpdateView):
    template_name = 'restaurans/restaurant_edit.html'
    form_class = RestProfileForm
    success_url = reverse_lazy('restaurans:restaurant-edit')

    def get_object(self, queryset=None):
        return self.request.user.restaurant  # Получаем ресторан текущего пользователя

    def form_valid(self, form):
        form.save()  # Сохраняем данные ресторана
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.request.user.restaurant.name} Редактирование'
        context['dishes'] = Dish.objects.filter(restaurant=self.request.user.restaurant).order_by("id")
        return context
