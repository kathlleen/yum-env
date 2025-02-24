from django.urls import path
from orders.consumers import OrderConsumer

websocket_urlpatterns = [
    path("ws/orders/<int:restaurant_id>/", OrderConsumer.as_asgi()),
]
