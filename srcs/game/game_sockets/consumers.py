import json
import random
import math 
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
 
class LobbyConsumer(WebsocketConsumer):
 
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
        self.game_state = {
            'type'
            'paddle_positions': {
                'player1': 50,
                'player2': 50,
            },
            'ball_position': {
                'x': 50,
                'y': 50,
            },
            'ball_speed': {
                'x': 5.5*random.choice([-1, 1]),
                'y': 5.5*random.choice([-1, 1]),
            },
        }
        self.send_game_state()
        self.running_game_loop = False
        self.connections = 0
        self.dx = 5
        self.paddle_offset = 0
        self.court_top = 0
        self.court_bottom = 0
        # The following attributes ar4e for the ball
        self.speed = 5.5
        self.dotX = 0
        self.dotY = 0
        self.dotKicked = False
 
    def connect(self):
        """
        Perform things on connection start
        """
        # self.message.reply_channel.send({"accept": True})
        self.room_name = self.scope["url_route"]["kwargs"]["room"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)( self.room_group_name, self.channel_name
        )
        # pass
        self.accept()
        self.connections += 1
        if not self.running_game_loop and self.connections >= 2:
            self.running_game_loop = True
            self.game_loop()
 
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        if message == "W" or message == "S":
            self.update_paddle_position("player1", message)
        if message == "UP" or message == "DOWN":
            self.update_paddle_position("player2", message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
 
    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
    
    async def game_loop(self):
        while self.running_game_loop:
            # Simulate ball movement, collision detection, and other game logic here
            self.update_ball_position()  # Update ball position
            await self.send_game_state()  # Broadcast the updated game state to all clients
            await asyncio.sleep(0.016)  # Sleep for 16ms (60 FPS)

    async def send_game_state(self):
        await self.send(json.dumps({'game_state': self.game_state}))
    """
    function moveRectangleRight(dx) {

    if (!dotKicked || rectRightPos + dx < court.offsetTop || rectRightPos + dx + rectangle_right.offsetHeight > court.offsetTop + pongCourtHeight) {
        return;
    }
    rectRightPos += dx;
    rectangle_right.style.top = `${rectRightPos}px`;
    }
    function moveRectangleLeft(dx) {
    if (!dotKicked || rectLeftPos + dx < court.offsetTop || rectLeftPos + dx + rectangle_left.offsetHeight > court.offsetTop + pongCourtHeight) {
        return;
    }
    rectLeftPos += dx;
    rectangle_left.style.top = `${rectLeftPos}px`;
    }
    """
    def update_paddle_position(self, player, action):
        if (self.game_state['paddle_positions'][player] + self.dx < self.court_top or
                self.game_state['paddle_positions'][player] + self.dx + self.paddle_offset> self.court_bottom):
            return
        if player == "player1":
            if action == "W":
                self.game_state['paddle_positions'][player] -= self.dx
            if action == "S":
                self.game_state['paddle_positions'][player] += self.dx
        if player == "player2":
            if action == "UP":
                self.game_state['paddle_positions'][player] -= self.dx
            if action == "DOWN":
                self.game_state['paddle_positions'][player] += self.dx
        ## Sent to the clients the new positions to update the front
         
        # Implement paddle position update logic here based on player input
        # Update self.game_state['paddle_positions'][player] accordingly

    def update_ball_position(self):
        # Implement ball movement and collis