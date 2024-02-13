import json
from channels.consumer import SyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from .engine import GameEngine

from game_matchmaking.models import Game
from django.db.models import Q

from urllib.parse import parse_qs
from .auth.jwt import validate_jwt_and_get_user_id

from asgiref.sync import async_to_sync, sync_to_async

import json
from django.core import serializers

 
class ClientConsumer(AsyncWebsocketConsumer):
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = "pong"
 
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

        games = []

        async for game in Game.objects.filter(Q(playerLeft=user_id) | Q(playerRight=user_id)).filter(Q(status=Game.GameStatus.WAITING)):
            games.append(game)

        if len(games) == 0:
            return await self.close()

        game = games[0]

        print(game)
        print(type(game))

        self.group_name = "game_" + str(game.id)

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.start(self.group_name, game)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        return await self.movement(message)

    # Receive message from room group
    async def game_update(self, event):
        print("game_update")
        game_dict = event["game_dict"]
        await self.send(text_data=json.dumps({"game_dict": game_dict}))

    async def start(self, group_name, game):
        await self.channel_layer.send("game_engine", {"type":"player.start",
                                                      "message": { "group_name":
                                                                  group_name,
                                                                  "game":
                                                                  serializers.serialize('json',
                                                                                        game.objects, )
                                                                  }})

    async def movement(self, msg: str):
        await self.channel_layer.send("game_engine", {"type":"player.movement" , "message": msg} )
 
    async def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.send(text_data=json.dumps({"message": "disconnected"}))
    
class GameConsumer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        """
        Created on demand when the first player joins.
        """
        print("Game Consumer: %s %s", args, kwargs)
        super().__init__(*args, **kwargs)
        self.group_name = "pong"
        self.engine = GameEngine(self.group_name)

    def player_start(self, event):
        msg = event.get("message")
        print(msg)
        if msg == "start" and not self.engine.is_alive():
            self.engine.start()
        self.engine.playerCount += 1
        # self.engine.players.append(self.engine.playerCount)
        if self.engine.playerCount == 2:
            self.engine.start()

    def player_movement(self, event):
        message = event.get("message")
        if message == "W" or message == "S":
            self.engine.update_paddle_position("left", message)
        if message == "UP" or message == "DOWN":
            self.engine.update_paddle_position("right", message)
        if message == "ENTER":
            self.engine.kick_dot()
