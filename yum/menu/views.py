from django.shortcuts import render, get_object_or_404

from restaurans.models import Restaurans
from menu.models import Dish


# Create your views here.
def menu(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurans, slug=restaurant_slug)
    dishes = Dish.objects.filter(restaurant=restaurant)

    context = {
        "title": restaurant.name,
        'page_description' : restaurant.description,
        "dishes" : dishes,

    }

    return render(request, 'menu/restaurant_menu.html', context)

def dish(request):
    pass