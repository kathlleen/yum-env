from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string

# Create your views here.

from carts.utils import get_user_carts

from carts.models import Cart
from django.urls import reverse
from menu.models import Dish
from restaurans.models import Restaurans


def cart_add(request):
    dish_id = request.POST.get("dish_id")
    restaurant_id = request.POST.get("rest_id")
    restaurant = get_object_or_404(Restaurans, id=restaurant_id)

    # dish_id = 5
    # print(dish_id)

    dish = Dish.objects.get(id=dish_id)
    # dish = get_object_or_404(Dish, pk=dish_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, dish=dish)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, dish=dish, quantity=1)

    else:
        carts = Cart.objects.filter(
            session_key=request.session.session_key, dish=dish)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(
                session_key=request.session.session_key, dish=dish, quantity=1)


    user_cart = get_user_carts(request, restaurant=restaurant)
    cart_items_html = render_to_string("includes/included_cart.html",
                                       {"carts": user_cart, "restaurant": restaurant}, request=request)

    response_data = {
        "cart_items_html": cart_items_html,
        "success": True # для тестирования
    }

    # return redirect(request.META['HTTP_REFERER'])
    return JsonResponse(response_data)


def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")
    rest_id = request.POST.get("rest_id")

    cart = Cart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()
    updated_quantity = cart.quantity

    if rest_id:
        restaurant = get_object_or_404(Restaurans, id=rest_id)
    else:
        restaurant = None

    user_cart = get_user_carts(request, restaurant=restaurant)

    context = {"carts": user_cart, "restaurant":restaurant}

    # # if referer page is create_order add key orders: True to context
    # referer = request.META.get('HTTP_REFERER')
    # if reverse('orders:create_order') in referer:
    #     context["order"] = True

    cart_items_html = render_to_string(
        "includes/included_cart.html", context, request=request)

    response_data = {
        "cart_items_html": cart_items_html,
        "quantity": updated_quantity,
    }

    return JsonResponse(response_data)


def cart_remove(request):
    cart_id = request.POST.get("cart_id")
    rest_id = request.POST.get("rest_id")

    cart = Cart.objects.get(id=cart_id)
    # quantity = cart.quantity
    cart.delete()

    if rest_id:
        restaurant = get_object_or_404(Restaurans, id=rest_id)
    else:
        restaurant = None

    user_cart = get_user_carts(request, restaurant=restaurant)
    cart_items_html = render_to_string("includes/included_cart.html",
                                       {"carts": user_cart, "restaurant": restaurant}, request=request)

    response_data = {
        "cart_items_html": cart_items_html,
        # "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)
    # return redirect(request.META['HTTP_REFERER'])


def cart_clear(request, restaurant_id):
    restaurant = get_object_or_404(Restaurans, id=restaurant_id)

    if request.user.is_authenticated:
        Cart.objects.filter(user=request.user, dish__restaurant=restaurant).delete()
    else:
        Cart.objects.filter(session_key=request.session.session_key, dish__restaurant=restaurant).delete()

    user_cart = get_user_carts(request, restaurant=restaurant)
    cart_items_html = render_to_string("includes/included_cart.html",
                                       {"carts": user_cart, "restaurant": restaurant}, request=request)

    return JsonResponse({"cart_items_html": cart_items_html, "success": True})