from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from couriers import views

app_name = 'couriers'

urlpatterns = [
    path('courier-dashboard/', views.courier_dashboard, name='courier-dashboard'),
    path('courier-profile/', views.CourierProfileView.as_view(), name='courier-profile'),
    path('courier-statistics/', views.courier_statistics, name='courier-statistics'),
    path('toggle-shift/', views.toggle_shift, name='toggle-shift'),
    path('update-location/', views.update_location, name='update-location'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
