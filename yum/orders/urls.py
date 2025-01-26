from django.urls import path

from orders.views import CreateOrderView

app_name = "orders"

urlpatterns = [
    # path('create-order/', views.create_order, name='create_order'),
    path('create-order/<int:restaurant_id>/', CreateOrderView.as_view(), name='create_order'),

]