from channels.generic.websocket import AsyncWebsocketConsumer
from .auth.jwt import validate_jwt_and_get_user_id
import json
import re
from django.contrib.auth.models import User


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        auth_header = list(filter(lambda x: x[0] == b'authorization', self.scope['headers']))
        if not auth_header:
            await self.close()

        extract = re.findall(r'^Bearer\s+(.*)$', auth_header[0][1].decode())
        if not extract:
            await self.close()

        jwt_token = extract[0]
        user_id = await validate_jwt_and_get_user_id(jwt_token)
        if not user_id:
            await self.close()

        self.id = user_id

        await self.channel_layer.group_add(
            f'group_{self.id}',
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            f'group_{self.id}',
            self.channel_name
        )

    async def send_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
