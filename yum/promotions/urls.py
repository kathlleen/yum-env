# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from promotions import views

app_name = 'promotions'

urlpatterns = [
    path('promotion-request/<int:restaurant_id>/', views.promotion_request_view, name='promotion_request'),
    path('edit/<int:pk>/', views.edit_promotion, name='edit_promotion')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)