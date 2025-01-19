from django import template

from carts.models import Cart
from decimal import Decimal, ROUND_HALF_UP
from carts.utils import get_user_carts, get_carts_restaurants

register = template.Library()

@register.simple_tag()
def user_carts(request, restaurant=None):
    return get_user_carts(request, restaurant)
@register.simple_tag()
def user_restaurants(request):
    return get_carts_restaurants(request)

@register.filter
def carts_courier_price(carts):
    price = sum(cart.dish.price * cart.quantity for cart in carts) * Decimal('0.05')
    return price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

@register.filter
def carts_total_price(carts):
    # Проверяем, что carts не пустой и это QuerySet
    if not carts:
        return Decimal(0)

    # Считаем общую стоимость
    total_price = sum(cart.dish.price * cart.quantity for cart in carts)
    return total_price