from django.urls import path

from main import views

app_name = 'restaurans'

urlpatterns = [
    # path('', views.index, name='index'),
    path('restauran-profile/', views.restauran_profile, name='restauran-profile'),
]
