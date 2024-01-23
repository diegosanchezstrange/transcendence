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
        self.running_game_loop = False
        self.connections = 0
        self.dx = 2
        self.paddle_right = 50
        self.paddle_left = 50
        self.court_top = 0
        self.court_bottom = 0
        # The following attributes ar4e for the ball
        self.dotX = 50
        self.dotY = 50
        ## send the initial state to the front to render the game

        self.speedX= 5.5*random.choice([-1, 1])
        self.speedY= 5.5*random.choice([-1, 1])
        self.dotKicked = False
        self.start = False
        self.game_state = {
            'paddle_right': self.paddle_left,
            'paddle_left': self.paddle_right,
            'ball':[self.dotX,self.dotY] 
        }
 
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
            self.update_paddle_position("left", message)
        if message == "UP" or message == "DOWN":
            self.update_paddle_position("right", message)
        #if message == "Enter":
            #self.kick_dot()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "game_dict": self.game_state}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["game_dict"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"game_dict": self.game_state}))
 
    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
    
    async def game_loop(self):
        await self.send_game_state()  # Broadcast the updated game state to all clients
        #while self.running_game_loop:
            # Simulate ball movement, collision detection, and other game logic here
            #self.update_ball_position()  # Update ball position
            #await asyncio.sleep(0.016)  # Sleep for 16ms (60 FPS)

    async def send_game_state(self):
        await self.send(json.dumps({'game_state': self.game_state}))

    def update_paddle_position(self, player, action):
        if action == "W" or action == "UP":
            if self.game_state['paddle_'+player] - self.dx-15 < 1:
                return
            self.game_state['paddle_'+player] -= self.dx
        elif action == "S" or action == "DOWN":
                if self.game_state['paddle_'+player] + self.dx + 15 > 99:
                    return
                self.game_state['paddle_'+player] += self.dx
        ## Sent to the clients the new positions to update the front
         
        # Implement paddle position update logic here based on player input
        # Update self.game_state['paddle_positions'][player] accordingly
    """
    function kickDot() {
    if (!dotKicked && !start){
        dotX = pongCourtWidth / 2 + court.offsetLeft - dot.offsetWidth / 2;
        dotY = pongCourtHeight / 2 +court.offsetTop- dot.offsetHeight / 2;
        dot.style.left = `${dotX}px`;
        dot.style.top = `${dotY}px`;
        dotSpeedX = vel * [1, -1].sample();
        dotSpeedY = vel* [1, -1].sample();
        rectangle_right.style.top = `${top_rect}px`;
        rectangle_left.style.top = `${top_rect}px`;
        rectRightPos = top_rect;
        rectLeftPos = top_rect;
        start = true
        return;
    }
    if (!dotKicked && start) {
        dotKicked = true;
        animateDot();
    }
    }
    """
    def kick_dot(self):
        if not self.dotKicked and not self.start:
            self.start = True
        elif not self.dotKicked and self.start:
            self.dotKicked = True
            self.update_ball_position()

    def update_ball_position(self):
        if not self.dotKicked:
            return
        

        # Implement ball movement and collitions logic here
