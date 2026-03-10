import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'admin_orders'

        # Check if user is staff (admin)
        if self.scope["user"].is_staff:
            # Join room group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            # Reject connection if not admin
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from room group
    async def order_message(self, event):
        message = event['message']
        order_data = event['order']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'order',
            'message': message,
            'order': order_data
        }))

    async def user_update_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_update',
            'message': event['message']
        }))
