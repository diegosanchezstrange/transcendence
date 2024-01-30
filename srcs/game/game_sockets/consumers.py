import json
import math 
from channels.consumer import SyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from .engine import GameEngine
 
class ClientConsumer(AsyncWebsocketConsumer):
 
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    # http_user = True
 
    # def connection_groups(self, **kwargs):
    #     """
    #     Called to return the list of groups to automatically add/remove
    #     this connection to/from.
    #     """
    #     return ["lobby"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connections = 0
        self.group_name = "pong"
        self.running_game_loop = False
 
    async def connect(self):
        #self.room_name = self.scope["url_route"]["kwargs"]["room"]
        #self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add( self.group_name, self.channel_name)
        # pass
        await self.accept()
        self.connections += 1
        print(self.connections)
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
        print("START")
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
    
    

        ## Sent to the clients the new positions to update the front
         
        # Implement paddle position update logic here based on player input


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
        if msg == "start":
            self.engine.run()

    def player_movement(self, event):
        message = event.get("message")
        print(message)
        if message == "W" or message == "S":
            print("right")
            self.engine.update_paddle_position("left", message)
        if message == "UP" or message == "DOWN":
            print("left")
            self.engine.update_paddle_position("right", message)
        if message == "ENTER":
            print("ENTER")
            self.engine.kick_dot()
    
        # Runs the engine in a new thread
            # Simulate ball movement, collision detection, and other game logic here
    # Update self.game_state['paddle_positions'][player] accordingly
