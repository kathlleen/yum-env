from django.urls import path

from menu import views

app_name = 'menu'

urlpatterns = [
    path('<slug:restaurant_slug>/', views.menu, name='restaurans_menu'),
    path('dish', views.dish, name='dish'),
]
