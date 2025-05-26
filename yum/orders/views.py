from django.shortcuts import get_object_or_404, redirect
from django.forms import ValidationError
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from carts.models import Cart
from orders.models import Order, OrderItem
from restaurans.models import Restaurans
from orders.forms import CreateOrderForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from geopy.distance import geodesic

from users.models import CustomUser


class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('users:profile')

    def dispatch(self, request, *args, **kwargs):
        # Get the restaurant object or raise 404 if not found
        self.restaurant = get_object_or_404(Restaurans, id=kwargs.get('restaurant_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        restaurant_id = self.kwargs.get('restaurant_id')
        cart_items = Cart.objects.filter(user=user, dish__restaurant_id=restaurant_id)

        if not cart_items.exists():
            messages.error(self.request, "Корзина пуста.")
            return redirect('orders:create_order', restaurant_id=restaurant_id)

        try:
            with transaction.atomic():
                # Create the order

                street = form.cleaned_data['street']
                house = form.cleaned_data['house']
                delivery_address = 'улица ' + street + ', ' + house

                order = Order.objects.create(
                    customer=user,
                    courier=None,
                    phone_number=form.cleaned_data['phone_number'],
                    delivery_address=delivery_address,
                    entrance=form.cleaned_data['entrance'],
                    floor=form.cleaned_data['floor'],
                    apartment=form.cleaned_data['apartment'],
                    payment_on_get=form.cleaned_data['payment_on_get'],
                    restaurant=self.restaurant,
                    status='processing'
                )

                # Create order items
                for cart_item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        dish=cart_item.dish,
                        name=cart_item.dish.name,
                        price=cart_item.dish.sell_price(),
                        quantity=cart_item.quantity,
                    )

                # Clear the cart
                cart_items.delete()

                available_couriers = CustomUser.objects.filter(
                    on_shift=True,
                    role='courier',
                    latitude__isnull=False,
                    longitude__isnull=False
                )

                if available_couriers.exists():
                    restaurant_location = (self.restaurant.latitude, self.restaurant.longitude)

                    sorted_couriers = sorted(
                        available_couriers,
                        key=lambda c: (
                            geodesic(restaurant_location, (c.latitude, c.longitude)).km,
                            c.priority
                        )
                    )
                    best_courier = sorted_couriers[0]
                    order.courier = best_courier
                    order.save()

                    # WebSocket уведомление курьеру
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        f"courier_{best_courier.id}",
                        {
                            "type": "new_order",
                            "order_id": order.id,
                            "restaurant": self.restaurant.name,
                            "address": order.delivery_address,
                        }
                    )
                    print("Отправляю сообщение ресторану:", f"restaurant_{order.restaurant.id}")
                    async_to_sync(channel_layer.group_send)(
                        f"restaurant_{order.restaurant.id}",
                        {
                            "type": "new_order",
                            "order_id": order.id,
                            "delivery_address": order.delivery_address,
                            "created_at": order.created_timestamp.strftime('%Y-%m-%d %H:%M'),
                        }
                    )



                return redirect(self.success_url)

        except ValidationError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

    def get_initial(self):
        # Pre-fill form with user data
        return {
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        context['restaurant'] = self.restaurant
        context['order'] = True
        return context
