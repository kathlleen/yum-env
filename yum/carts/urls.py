from django.contrib import admin
from django.urls import path

from carts import views
app_name = "carts"

urlpatterns = [
    # path('', views.catalog, name='index'),
    path('cart_add/<int:dish_id>/', views.cart_add, name='cart_add'),
    path('cart_change/', views.cart_change, name='cart_change'),
    path('cart_remove/<int:cart_id>/', views.cart_remove, name='cart_remove')

]