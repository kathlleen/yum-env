from django.urls import path

from restaurans import views

app_name = 'restaurans'

urlpatterns = [
    path('restaurant-dashboard/', views.restaurant_dashboard, name='restaurant-dashboard'),
]
