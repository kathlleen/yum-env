from django.urls import path

from main import views

from main.views import IndexView

app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', IndexView.as_view(), name='search'),
    path('filter_restaurants/<str:category_slug>/', views.filter_restaurants, name='filter_restaurants'),
    path('filter_by_cuisine/<str:cuisine_slug>/', views.filter_by_cuisine, name='filter_by_cuisine'),
    path('promotion-detail/<int:promo_id>/', views.promotion_detail, name='promotion_detail'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('about/', views.about, name='about'),
    path('<slug:category_slug>/', IndexView.as_view(), name='index'),
]
