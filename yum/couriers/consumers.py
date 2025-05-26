# couriers/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CourierConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.courier_id = self.scope["url_route"]["kwargs"]["courier_id"]
        self.group_name = f"courier_{self.courier_id}"

        # Присоединение к группе
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Отсоединение от группы
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def new_order(self, event):
        await self.send(text_data=json.dumps({
            "type": "new_order",
            "order_id": event["order_id"],
            "restaurant": event["restaurant"],
            "address": event["address"]
        }))
