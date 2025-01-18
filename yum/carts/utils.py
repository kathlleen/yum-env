from carts.models import Cart


def get_user_carts(request, restaurant=None):
    if request.user.is_authenticated:
        query = Cart.objects.filter(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        query = Cart.objects.filter(session_key=request.session.session_key)

    if restaurant:
        query = query.filter(dish__restaurant=restaurant)


    return query