"""
URL configuration for yum project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static

from yum import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('user/', include('users.urls', namespace='users')),
    path('cart/', include('carts.urls', namespace='cart')),
    path('menu/', include('menu.urls', namespace='menu')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('restaurans/', include('restaurans.urls', namespace='restaurans')),
    path('couriers/', include('couriers.urls', namespace='couriers')),
    path('promotions/', include('promotions.urls', namespace='promotions')),
    path('selections/', include('rest_collections.urls', namespace='selections')),
]


handler404 = views.handler404
handler500 = views.handler500

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)