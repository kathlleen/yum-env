from carts.models import Cart


def get_user_carts(request, restaurant=None):
    if request.user.is_authenticated:
        query = Cart.objects.filter(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        query = Cart.objects.filter(session_key=request.session.session_key)

    query = query.filter(dish__restaurant=restaurant)

    return query

# Получаем все рестораны, корзины которых есть у пользователя
def get_carts_restaurants(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        carts = Cart.objects.filter(session_key=request.session.session_key)

    restaurants = {cart.dish.restaurant for cart in carts if cart.dish and cart.dish.restaurant}

    print(f'Rest {restaurants}')

    return list(restaurants)