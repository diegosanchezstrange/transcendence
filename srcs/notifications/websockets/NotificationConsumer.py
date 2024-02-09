from channels.generic.websocket import AsyncWebsocketConsumer
from .auth.jwt import validate_jwt_and_get_user_id
import json
# import re
from django.contrib.auth.models import User

import requests
from notifications import settings
from urllib.parse import parse_qs
from channels.db import database_sync_to_async



class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #Get the token from the query string
        query_string = self.scope["query_string"]
        query_params = query_string.decode()
        query_dict = parse_qs(query_params)
        try:
            jwt_token = query_dict["token"][0]
        except:
            await self.close()
            raise Exception("Token not found")

        # Find the user from the token in the database
        user_id = await validate_jwt_and_get_user_id(jwt_token)
        if not user_id:
            await self.close()
            return

        # user = User.objects.get(pk=user_id)

        user = await database_sync_to_async(User.objects.get)(pk=user_id)
        self.id = user_id

        # Create a group named "group_<user_id>"
        await self.channel_layer.group_add(
            f'group_{self.id}',
            self.channel_name
        )

        # Create a group for global notifications
        await self.channel_layer.group_add(
            f'broadcast',
            self.channel_name
        )

        # Send a message to your friends that you are online
        headers = {
            "Authorization": f"Bearer {jwt_token}"
        }
        friends = requests.get(settings.USERS_SERVICE_HOST + f"/friends/", headers=headers).json()["detail"]

        for friend in friends:
            await self.channel_layer.group_send(
                f'group_{friend["id"]}',
                {
                    'type': 'send_message',
                    'message': f'{user.username} is online'
                }
            )

        await self.accept()

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            f'group_{self.id}',
            self.channel_name
        )

    async def send_message(self, event):


        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
