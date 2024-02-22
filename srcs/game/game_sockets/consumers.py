import json
from channels.consumer import SyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from .engine import GameEngine

from game_matchmaking.models import Game, GameInvite
from django.db.models import Q

from urllib.parse import parse_qs
from .auth.jwt import validate_jwt_and_get_user_id

from asgiref.sync import async_to_sync, sync_to_async
from channels.db import database_sync_to_async

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
        self.user_id = user_id

        print("User id: ", user_id)

        # Check the query parameters for the game id or invite id
        game_id = query_dict.get("game", None)
        invite_id = query_dict.get("invitation", None)

        if game_id:
            try:
                game_id = int(game_id[0])
                game = await database_sync_to_async(Game.objects.get)(id=game_id)
                playerLeft_id = await sync_to_async(lambda: game.playerLeft.id)()
                playerRight_id = await sync_to_async(lambda: game.playerRight.id)()
                self.group_name = "game_" + str(playerLeft_id) + "_" + str(playerRight_id)
            except Game.DoesNotExist:
                await self.close()
                return
            except Exception as e:
                print(e)
                await self.close()
                return
        elif invite_id:
            try:
                invite_id = int(invite_id[0])
                invite = await database_sync_to_async(GameInvite.objects.get)(id=invite_id)
                sender_id = await sync_to_async(lambda: invite.sender.id)()
                receiver_id = await sync_to_async(lambda: invite.receiver.id)()
                self.group_name = "game_" + str(sender_id) + "_" + str(receiver_id)
            except GameInvite.DoesNotExist:
                await self.close()
                return
            except Exception as e:
                print(e)
                await self.close()
                return
        else:
            await self.close()
            return

        print("Group name: ", self.group_name)

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        await self.start(self.group_name, user_id, game_id, invite_id)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        return await self.movement(message)

    # Receive message from room group
    async def game_update(self, event):
        # print("game_update " + self.group_name)
        game_dict = None
        try:
            game_dict = event["game_dict"]
            await self.send(text_data=json.dumps({"game_dict": game_dict}))
        except:
            pass
        try:
            game_dict = event["score_dict"]
            await self.send(text_data=json.dumps({"score_dict": game_dict}))
        except:
            pass
        try:
            game_dict = event["end_dict"]
            await self.send(text_data=json.dumps({"end_dict": game_dict}))
            await self.channel_layer.send("game_engine", {"type":"game.end",
                                          "message": { "group_name":
                                                      self.group_name
                                                      }})
            await self.close()
        except:
            pass

    async def start(self, group_name, user_id, game_id=None, invite_id=None):
        await self.channel_layer.send("game_engine", {"type":"player.start",
                                                      "message": { "group_name":
                                                                  group_name,
                                                                  "user_id":
                                                                  user_id,
                                                                  "game_id":
                                                                    game_id,
                                                                  "invite_id":
                                                                    invite_id
                                                                  }})

    async def movement(self, msg: str):
        await self.channel_layer.send("game_engine", {"type":"player.movement" ,
                                                      "message": msg,
                                                      "user_id": self.user_id,
                                                      "group_name" : self.group_name} )
 
    async def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        # await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.channel_layer.send("game_engine", {"type":"player.disconnect",
                                                        "message": { "group_name":
                                                                    self.group_name,
                                                                    "user_id": self.user_id
                                                                    }})
    
class GameConsumer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        """
        Created on demand when the first player joins.
        """
        # print("Game Consumer: %s %s", args, kwargs)
        super().__init__(*args, **kwargs)
        self.group_name = "pong"
        self.engine = GameEngine(self.group_name)
        self.engine.start()

    def player_start(self, event):
        msg = event.get("message")
        print(msg)
        game_id = msg.get("game_id")
        invite_id = msg.get("invite_id")
        self.engine.add_player(msg.get("group_name"), msg.get("user_id"), game_id, invite_id)

    def player_disconnect(self, event):
        msg = event.get("message")
        print(msg)
        self.engine.remove_player(msg.get("group_name"), msg.get("user_id"))

    def game_end(self, event):
        msg = event.get("message")
        print(msg)
        self.engine.end_game(msg.get("group_name"))

    def player_movement(self, event):
        message = event.get("message")
        group_name = event.get("group_name")
        user_id = event.get("user_id")
        self.engine.update_paddle_position(user_id, message, group_name)
        if message == "ENTER":
            self.engine.kick_dot(group_name)
