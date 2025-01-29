from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from restaurans import views

app_name = 'restaurans'

urlpatterns = [
    path('restaurant-dashboard/', views.restaurant_dashboard, name='restaurant-dashboard'),
    path('restaurant-edit/', views.RestEditView.as_view(), name='restaurant-edit'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)