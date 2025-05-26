# restaurants/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RestaurantConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.restaurant_id = self.scope["url_route"]["kwargs"]["restaurant_id"]
        self.group_name = f"restaurant_{self.restaurant_id}"


        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        print(">> Подключение ресторана:", self.group_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Пример: уведомление, что заказ доставлен
    async def new_order(self, event):
        print(">>> NEW ORDER EVENT", event)
        await self.send(text_data=json.dumps({
            "type": "new_order",
            "order_id": event["order_id"],
            "delivery_address": event["delivery_address"],
            "created_at": event["created_at"],
        }))
