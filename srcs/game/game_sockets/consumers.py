import json
from channels.consumer import SyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from .engine import GameEngine
 
class ClientConsumer(AsyncWebsocketConsumer):
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connections = 0
        self.group_name = "pong"
        self.running_game_loop = False
 
    async def connect(self):
        # Join room group
        await self.channel_layer.group_add( self.group_name, self.channel_name)
        # pass
        await self.accept()
        self.connections += 1
        if self.connections >= 1:
            self.running_game_loop = True
            await self.start()
 
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        return await self.movement(message)

    # Receive message from room group
    async def game_update(self, event):
        game_dict = event["game_dict"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"game_dict": game_dict}))

    async def start(self):
        await self.channel_layer.send("game_engine", {"type":"player.start", "message": "start"})

    async def movement(self, msg: str):
        if not self.running_game_loop:
            return
        await self.channel_layer.send("game_engine", {"type":"player.movement" , "message": msg} )
 
    async def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
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
        if msg == "start" and not self.engine.is_alive():
            self.engine.start()
        self.engine.playerCount += 1
        self.engine.players.append(self.engine.playerCount)

    def player_movement(self, event):
        message = event.get("message")
        if message == "W" or message == "S":
            self.engine.update_paddle_position("left", message)
        if message == "UP" or message == "DOWN":
            self.engine.update_paddle_position("right", message)
        if message == "ENTER":
            self.engine.kick_dot()
