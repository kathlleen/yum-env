from django.urls import path

from rest_collections import views

app_name = 'selections'

urlpatterns = [
    path('selection_restaurants/<str:selection_slug>/', views.selection_restaurants, name='selection_restaurants'),
]
