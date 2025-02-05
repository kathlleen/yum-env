from django.urls import path

from menu.views import MenuView, DishDetailView
from restaurans.views import DeleteDishView

app_name = 'menu'

urlpatterns = [
    path('<slug:restaurant_slug>/', MenuView.as_view(), name='restaurans_menu'),
    path('<slug:restaurant_slug>/dish-detail/<int:dish_id>/', DishDetailView.as_view(), name='dish_detail'),
]
