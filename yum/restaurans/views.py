from django.conf import settings
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.views import View
from orders.models import Order

from django.views.generic.edit import FormView
from menu.models import Dish

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from common.mixins import CacheMixin

from restaurans.forms import DishForm, CategoryForm, RestProfileForm


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


    def get_success_url(self):
        return reverse_lazy('restaurans:restaurant-edit')  # После сохранения вернёт на страницу ресторана

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование {self.object.name}'
        context['restaurant'] = self.request.user.restaurant
        return context

class AddDishView(LoginRequiredMixin, View):
    def get(self, request):
        form = DishForm()
        context = {'form': form, 'restaurant': self.request.user.restaurant}
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

