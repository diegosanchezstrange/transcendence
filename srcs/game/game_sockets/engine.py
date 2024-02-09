import threading
import random
import time

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class GameEngine(threading.Thread):

    playerCount = 0

    players = []

    def __init__(self, channel_name, **kwargs):
        super(GameEngine, self).__init__(daemon=True, name="GameEngine", **kwargs)
        self.dx = random.choice([0.5, 1])
        self.group_name = channel_name  
        self.dy = random.choice([0.5, 1])
        self.channel_layer = get_channel_layer()
        self.paddle_right = 50
        self.paddle_left = 50
        self.court_top = 0
        self.court_bottom = 0
        # The following attributes ar4e for the ball
        self.dotX = 50
        self.dotY = 50
        ## send the initial state to the front to render the game

        self.speedX= self.dx*random.choice([-1, 1])
        self.speedY= self.dy*random.choice([-1, 1])
        self.started = True
        self.dotKicked = False
        #self.start = False
        self.game_state = {
            'paddle_right': self.paddle_left,
            'paddle_left': self.paddle_right,
            'ball':[self.dotX,self.dotY] 
        }

    def run(self) -> None:
        while True:
            self.update_ball_position()  # Update ball position
            self.broadcast_state()
            time.sleep(0.016)

    def broadcast_state(self):
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "game_update", "game_dict": self.game_state}
        )
    def restart_state(self):
        self.dotX = 50
        self.dotY = 50
        self.speedX = self.dx*random.choice([-1, 1])
        self.speedY = self.dy*random.choice([-1, 1])
        #restart the position of the paddles
        self.paddle_right = 50
        self.paddle_left = 50
        self.game_state['paddle_right'] = self.paddle_right
        self.game_state['paddle_left'] = self.paddle_left
        self.game_state['ball'] = [self.dotX, self.dotY]
        self.dotKicked = False

    def kick_dot(self):
        if not self.started and not self.dotKicked:
            self.restart_state()
            self.started = True
        elif self.started and not self.dotKicked:
            self.dotKicked = True 

    def update_ball_position(self):
        if not self.dotKicked:
            return
        # loosing because of coliision with the left wall
        if (self.dotX + self.speedX - 0.5) < 1:
            self.dotKicked = False
            self.started = False
        # loosing because of coliision with the right wall
        elif (self.dotX + self.speedX + 0.5) > 99:
            self.dotKicked = False
            self.started = False
        #bouncing at the top
        elif (self.dotY + self.speedY - 0.5) < 1:
            self.speedY = -self.speedY
            self.dotY += self.speedY
        # bouncing at the bottom
        elif (self.dotY + self.speedY + 0.5) > 99:
            self.speedY = -self.speedY
            self.dotY += self.speedY
        # bouncing at the right paddle
        elif (self.dotX + self.speedX + 0.5) > 93 and (self.paddle_right - 15) < self.dotY < (self.paddle_right + 15):
            self.speedX = -self.speedX
            self.dotX += self.speedX
        # bouncing at the left paddle
        elif (self.dotX + self.speedX - 0.5) < 7 and (self.paddle_left - 15) < self.dotY < (self.paddle_left + 15):
            print("left paddle")
            self.speedX = -self.speedX
            self.dotX += self.speedX
        #regular movement
        else:
            self.dotY += self.speedY
            self.dotX += self.speedX
        self.game_state['ball'] = [self.dotX, self.dotY] 

    def update_paddle_position(self, player, action):
        if action == "W" or action == "UP":
            if self.game_state['paddle_'+player] - self.dx-15 < 1:
                return
            self.game_state['paddle_'+player] -= self.dx
        elif action == "S" or action == "DOWN":
            if self.game_state['paddle_'+player] + self.dx + 15 > 99:
                return
            self.game_state['paddle_'+player] += self.dx
        self.paddle_right = self.game_state['paddle_right']
        self.paddle_left = self.game_state['paddle_left']
