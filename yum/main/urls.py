from django.urls import path

from main import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),

    path('about/', views.about, name='about'),
    path('<slug:category_slug>/', views.index, name='index'),
]
