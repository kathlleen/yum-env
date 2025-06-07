from collections import defaultdict
from datetime import timedelta

from _decimal import Decimal
from django.conf import settings
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from orders.models import Order
from menu.models import Label
from django.views.generic.edit import FormView
from menu.models import Dish
from django.utils.timezone import now, timedelta
from django.db.models import Sum, Avg, Count, F
from orders.models import Order, OrderItem, OrderRating
from menu.models import Dish

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from common.mixins import CacheMixin

from restaurans.forms import DishForm, CategoryForm, RestProfileForm

from orders.models import OrderItem


def is_restaurant_admin(user):
    return user.is_authenticated and user.is_restaurant_admin()
@login_required
@user_passes_test(is_restaurant_admin, login_url='main:index')
def restaurant_dashboard(request):
    restaurant = request.user.restaurant

    if not restaurant:
        return redirect('main:index')

    # Используем значения из STATUS_CHOICES для фильтрации
    orders = Order.objects.filter(restaurant=restaurant).order_by('-id')
    process_orders = orders.filter(status='processing')
    wait_orders = orders.filter(status='awaiting_delivery')

    context = {
        'title': f'{restaurant.name} Админ',
        'restaurant': restaurant,
        'process_orders': process_orders,
        'wait_orders': wait_orders
    }

    return render(request, 'restaurans/restaurant_dashboard.html', context)




@login_required
@user_passes_test(is_restaurant_admin, login_url='main:index')
def restaurant_statistics(request):
    user = request.user
    restaurant = user.restaurant

    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    orders = Order.objects.filter(restaurant=restaurant)

    # Заказы
    orders_today = orders.filter(created_timestamp__date=today).count()
    orders_week = orders.filter(created_timestamp__date__gte=start_of_week).count()
    orders_month = orders.filter(created_timestamp__date__gte=start_of_month).count()

    # Прибыль
    items = OrderItem.objects.filter(order__restaurant=restaurant)
    earned_today = items.filter(created_timestamp__date=today).aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0
    earned_week = items.filter(created_timestamp__date__gte=start_of_week).aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0
    earned_month = items.filter(created_timestamp__date__gte=start_of_month).aggregate(total=Sum(F('price') * F('quantity')))['total'] or 0

    # Рейтинг
    avg_rating = OrderRating.objects.filter(restaurant=restaurant).aggregate(avg=Avg('restaurant_rating'))['avg']

    # Популярные блюда
    top_dishes = (
        items.values('dish__name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')[:5]
    )

    # Данные для графиков
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    orders_labels = [d.strftime("%d.%m") for d in last_7_days]
    orders_data = [orders.filter(created_timestamp__date=d).count() for d in last_7_days]
    revenue_data = [
        float(items.filter(created_timestamp__date=day).aggregate(
            total=Sum(F('price') * F('quantity'))
        )['total'] or 0)
        for day in last_7_days
    ]

    context = {
        'restaurant': restaurant,
        'orders_today': orders_today,
        'orders_week': orders_week,
        'orders_month': orders_month,

        'earned_today': round(earned_today, 2),
        'earned_week': round(earned_week, 2),
        'earned_month': round(earned_month, 2),

        'avg_rating': round(avg_rating, 1) if avg_rating else None,
        'top_dishes': top_dishes,

        'orders_labels': orders_labels,
        'orders_data': orders_data,
        'revenue_data': revenue_data,
    }

    return render(request, 'restaurans/restaurant_statistics.html', context)

@login_required
@user_passes_test(is_restaurant_admin, login_url='main:index')
def mark_order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status == 'processing':
        order.status = 'awaiting_delivery'
        order.save()
    elif order.status == 'awaiting_delivery':
        order.status = 'on_the_way'
        order.save()

    return redirect('restaurans:restaurant-dashboard')


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
        context['api_key'] = settings.API_KEY
        context['restaurant'] = self.request.user.restaurant
        context['address'] = self.request.user.restaurant.address.replace(' ', '+')
        return context

class EditDishView(LoginRequiredMixin, UpdateView):
    model = Dish
    template_name = 'restaurans/edit_dish.html'
    form_class = DishForm
    context_object_name = 'dish'

    def form_valid(self, form):
        response = super().form_valid(form)

        selected_labels = self.request.POST.getlist('labels')
        self.object.labels.set(selected_labels)  # Привязываем метки к блюду

        return response

    def get_success_url(self):
        return reverse_lazy('restaurans:restaurant-edit')  # После сохранения вернёт на страницу ресторана

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование {self.object.name}'
        context['restaurant'] = self.request.user.restaurant

        grouped_labels = defaultdict(list)
        for label in Label.objects.all():
            grouped_labels[label.get_type_display()].append(label)

        context['grouped_labels'] = grouped_labels
        print(grouped_labels)

        return context

class AddDishView(LoginRequiredMixin, View):
    def get(self, request):
        form = DishForm()

        grouped_labels = defaultdict(list)
        for label in Label.objects.all():
            grouped_labels[label.get_type_display()].append(label)


        context = {
            'form': form,
            'restaurant': self.request.user.restaurant,
            'grouped_labels': grouped_labels
            }
        return render(request, 'restaurans/add_dish.html', context)

    def post(self, request):
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            dish = form.save(commit=False)
            dish.restaurant = request.user.restaurant  # Привязываем блюдо к ресторану пользователя
            dish.save()
            return redirect('restaurans:restaurant-edit')  # Перенаправление на страницу с меню ресторана
        return render(request, 'restaurans/add_dish.html', {'form': form})

class AddCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        form = CategoryForm()
        context = {'form': form, 'restaurant': self.request.user.restaurant}
        return render(request, 'restaurans/add_category.html', context)

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurans:restaurant-edit')  # Перенаправление после добавления
        return render(request, 'restaurans/add_category.html', {'form': form})



class DeleteDishView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, *args, **kwargs):
        dish = get_object_or_404(Dish, slug=self.kwargs["slug"])

        if request.user.restaurant != dish.restaurant:
            return JsonResponse({"success": False, "error": "Доступ запрещен"}, status=403)

        dish.delete()
        return JsonResponse({"success": True})

    def test_func(self):
        dish = get_object_or_404(Dish, slug=self.kwargs["slug"])
        return self.request.user.restaurant == dish.restaurant

