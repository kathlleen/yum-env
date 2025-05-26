from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"^ws/courier/(?P<courier_id>\d+)/$", consumers.CourierConsumer.as_asgi()),
]
