from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from restaurans import views
from restaurans.views import AddCategoryView

app_name = 'restaurans'

urlpatterns = [
    path('restaurant-dashboard/', views.restaurant_dashboard, name='restaurant-dashboard'),
    path('restaurant-edit/', views.RestEditView.as_view(), name='restaurant-edit'),
    path('edit-dish/<slug:slug>/', views.EditDishView.as_view(), name='edit-dish'),
    path('dish/<slug:slug>/delete/', views.DeleteDishView.as_view(), name='delete-dish'),
    path('add-dish/', views.AddDishView.as_view(), name='add-dish'),
    path('add-category/', AddCategoryView.as_view(), name='add-category'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)