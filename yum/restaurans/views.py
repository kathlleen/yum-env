from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.views import View
from orders.models import Order

from django.views.generic.edit import FormView
from menu.models import Dish

from users.forms import RestProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from common.mixins import CacheMixin

from restaurans.forms import DishForm

from restaurans.forms import CategoryForm


def is_restaurant_admin(user):
    return user.is_authenticated and user.is_restaurant_admin()


@login_required
@user_passes_test(is_restaurant_admin, login_url='main:index')
def restaurant_dashboard(request):
    # Проверяем, что пользователь связан с рестораном
    restaurant = request.user.restaurant

    if not restaurant:
        return redirect('main:index')  # Перенаправляем, если у пользователя нет ресторана

    # Получаем заказы для ресторана
    orders = Order.objects.filter(restaurant=restaurant).order_by('-id')
    process_orders = orders.filter(status='Процесс')
    wait_orders = orders.filter(status='Ждет курьера')

    context = {
        'title': f'{restaurant.name} Админ',
        'restaurant': restaurant,
        'process_orders': process_orders,  # Передаем заказы в шаблон
        'wait_orders' : wait_orders
    }

    return render(request, 'restaurans/restaurant_dashboard.html', context)

@login_required
@user_passes_test(is_restaurant_admin, login_url='main:index')
def mark_order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Меняем статус заказа
    if order.status == 'Процесс':
        order.status = 'Ждет курьера'
        order.save()
        return redirect('restaurans:restaurant-dashboard')
    if order.status == 'Ждет курьера':
        order.status = 'В пути'
        order.save()
        return redirect('restaurans:restaurant-dashboard')  # Перезагружаем страницу

# def restaurant_edit(request):
#     restaurant = request.user.restaurant
#
#     dishes = Dish.objects.filter(restaurant=restaurant)
#
#     if not restaurant:
#         return redirect('main:index')
#
#     context = {
#         'title': f'{restaurant.name} Редактирование',
#         'restaurant': restaurant,
#         'dishes': dishes,  # Передаем заказы в шаблон
#     }
#
#     return render(request, 'restaurans/restaurant_edit.html', context)


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

class EditDishView(LoginRequiredMixin, UpdateView):
    model = Dish
    template_name = 'restaurans/edit_dish.html'
    form_class = DishForm
    context_object_name = 'dish'

    def get_success_url(self):
        return reverse_lazy('restaurans:restaurant-edit')  # После сохранения вернёт на страницу ресторана

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование {self.object.name}'
        return context

class AddDishView(LoginRequiredMixin, View):
    def get(self, request):
        form = DishForm()
        return render(request, 'restaurans/add_dish.html', {'form': form})

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
        return render(request, 'restaurans/add_category.html', {'form': form})

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

