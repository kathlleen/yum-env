from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users import views

app_name = 'users'

urlpatterns = [
    # path('', views.index, name='index'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/customer/', views.CustomerRegistrationView.as_view(), name='register_customer'),
    path('register/restaurant_admin/', views.RestaurantAdminRegistrationView.as_view(), name='register_restaurant_admin'),
    path('register/courier/', views.CourierRegistrationView.as_view(), name='register_courier'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    # path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),
    # path('dashboard/courier/', views.courier_dashboard, name='courier_dashboard'),
]
