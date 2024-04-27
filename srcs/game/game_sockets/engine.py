import threading
import random
import time

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from game_matchmaking.models import Game, GameInvite, Tournament, UserTournament
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

import requests

class GameInstance():
    def __init__(self, group_name):
        self.channel_layer = get_channel_layer()

        self.game_id = None
        self.invite_id = None

        self.game: Game
        self.invite = None

        # Game status
        self.dx = random.choice([0.5, 1])
        self.group_name = group_name
        self.dy = random.choice([0.5, 1])
        self.paddle_right = 50
        self.paddle_left = 50
        self.court_top = 0
        self.court_bottom = 0
        # The following attributes ar4e for the ball
        self.dotX = 50
        self.dotY = 50

        self.speedX= self.dx*random.choice([-1, 1])
        self.speedY= self.dy*random.choice([-1, 1])
        self.started = True
        self.dotKicked = False

        self.game_state = {
            'paddle_right': self.paddle_left,
            'paddle_left': self.paddle_right,
            'ball':[self.dotX,self.dotY] 
        }

        self.status = self.GameStatus.WAITING

        self.playerLeftId = int(self.group_name.split("_")[1])
        self.playerRightId = int(self.group_name.split("_")[2])

        self.playerLeftStatus = self.PlayerStatus.WAITING
        self.playerRightStatus = self.PlayerStatus.WAITING

        self.playerLeftScore = 0
        self.playerRightScore = 0

        self.disconnection_time = None
        self.start_time = timezone.now()
        self.connection_time = None

    class GameStatus():
        WAITING = "WAITING"
        PLAYING = "IN_PROGRESS"
        PAUSED = "PAUSED"
        FINISHED = "FINISHED"
    class PlayerStatus():
        WAITING = "waiting"
        PLAYING = "playing"
        DISCONNECTED = "disconnected"
        FINISHED = "finished"

    # Custon exception
    class GameError(Exception):
        pass
    class GameNotFoundError(GameError):
        pass
    class GameMismatchError(GameError):
        pass
    class PlayersDisconnectedError(GameError):
        pass

    def add_player(self, user_id, game_id, invite_id):
        if game_id and self.game_id != game_id and self.game_id is not None:
            print("Error: game_id mismatch")
            raise self.GameMismatchError
        if invite_id and self.invite_id != invite_id and self.invite_id is not None:
            print("Error: invite_id mismatch")
            raise self.GameMismatchError

        if game_id:
            self.game_id = game_id
            try:
                self.game = Game.objects.get(id=game_id)
            except Game.DoesNotExist:
                print("Error: game not found")
                raise self.GameNotFoundError
        elif invite_id:
            self.invite_id = invite_id
            try:
                self.invite = GameInvite.objects.get(id=invite_id)
            except GameInvite.DoesNotExist:
                print("Error: invite not found")
                raise self.GameNotFoundError


        if self.playerLeftId == user_id:
            self.playerLeftStatus = self.PlayerStatus.PLAYING
            self.connection_time = timezone.now()
        elif self.playerRightId == user_id:
            self.playerRightStatus = self.PlayerStatus.PLAYING
            self.connection_time = timezone.now()

        if self.connection_time is not None:
            try:
                self.game.connection_time = self.connection_time
                self.game.save()
            except Exception as e:
                print("Error saving game: ", e)

        if self.playerLeftStatus == self.PlayerStatus.PLAYING and self.playerRightStatus == self.PlayerStatus.PLAYING:
            if self.game_id is None or self.game is None:
                print("Error: game_id or game not found on add_player")
                raise self.GameNotFoundError
            #Test exit
            self.started = True
            self.status = self.GameStatus.PLAYING
            self.game = Game.objects.get(id=self.game_id)
            self.game.status = Game.GameStatus.IN_PROGRESS
            self.game.save()
            
    def remove_player(self, user_id):
        if self.game.status == Game.GameStatus.FINISHED:
            self.status = self.GameStatus.FINISHED
            self.playerLeftStatus = self.PlayerStatus.FINISHED

        if self.playerLeftId == user_id:
            self.status = self.GameStatus.PAUSED
            self.playerLeftStatus = self.PlayerStatus.DISCONNECTED
        elif self.playerRightId == user_id:
            self.status = self.GameStatus.PAUSED
            self.playerRightStatus = self.PlayerStatus.DISCONNECTED

        if self.playerLeftStatus == self.PlayerStatus.DISCONNECTED and self.playerRightStatus == self.PlayerStatus.DISCONNECTED:
            try:
                self.game.playerLeftScore = self.playerLeftScore
                self.game.playerRightScore = self.playerRightScore
                self.game.status = Game.GameStatus.FINISHED
                self.game.save()
            except Exception as e:
                print("Error saving game: ", e)

            raise self.PlayersDisconnectedError

        try:
            self.game.playerLeftScore = self.playerLeftScore
            self.game.playerRightScore = self.playerRightScore
            self.game.status = Game.GameStatus.PAUSED
            self.game.disconnection_time = timezone.now()
            self.disconnection_time = self.game.disconnection_time
            self.game.save()
        except Exception as e:
            print("Error saving game: ", e)


    def player_side(self, user_id):
        if self.playerLeftId == user_id:
            return "left"
        elif self.playerRightId == user_id:
            return "right"
        return None

    def side_player(self, side):
        if side == "left":
            return self.playerLeftId
        elif side == "right":
            return self.playerRightId
        return None

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

    def player_scored(self, player_side):
        if player_side == "left":
            self.playerLeftScore += 1
            if (self.game):
                self.game.playerLeftScore = self.playerLeftScore
        elif player_side == "right":
            self.playerRightScore += 1
            if (self.game):
                self.game.playerRightScore = self.playerRightScore
        if self.playerLeftScore >= 5 or self.playerRightScore >= 5:
            print("Player won the game")
            try:
                winner_id = self.side_player(player_side)
                winner = User.objects.get(id=winner_id)
            except:
                winner = None
            if (self.game):
                self.game.winner = winner
            self.game_finished(self.side_player(player_side))
            if (self.game):
                self.game.save()
            if (self.game.tournament):
                loser_id = self.side_player("left" if player_side == "right" else "right")
                try:
                    loser = User.objects.get(id=loser_id)
                    user_tournament = UserTournament.objects.get(user=loser, tournament=self.game.tournament)
                    user_tournament.status = UserTournament.UserStatus.ELIMINATED
                    user_tournament.save()
                except Exception as e:
                    print("Error saving user tournament: ", e)

                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': settings.MICROSERVICE_API_TOKEN
                }

                new_game = requests.post(settings.GAME_SERVICE_HOST_INTERNAL +
                    '/tournament/nextgame/', headers=headers, json={
                        'tournament_id': self.game.tournament.id
                    }, verify=False)

    def game_winned_disconnected(self):
        if self.playerLeftStatus == self.PlayerStatus.DISCONNECTED:
            self.game_finished(self.playerRightId)
        elif self.playerRightStatus == self.PlayerStatus.DISCONNECTED:
            self.game_finished(self.playerLeftId)

    def game_not_contested(self):
        self.status = self.GameStatus.FINISHED
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "game_update", "end_dict": {"end": "Game not contested", "winner": None}}
        )
        try:
            self.game.status = Game.GameStatus.FINISHED
            self.game.winner = None
            self.game.save()
        except:
            pass

    def game_finished(self, winner_id):
        self.status = self.GameStatus.FINISHED


        try:
            tournament_id = self.game.tournament.id
            if tournament_id:
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name, {"type": "game_update", "end_dict": {"end": "Game finished", "winner": winner_id, "tournament_id": tournament_id}}
                )
            else:
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name, {"type": "game_update", "end_dict": {"end": "Game finished", "winner": winner_id}}
                )
        except Exception as e:
            print("Error sending game update: ", e)
        try:
            self.game.status = Game.GameStatus.FINISHED
            self.game.winner = User.objects.get(id=winner_id)
            self.game.playerLeftScore = self.playerLeftScore
            self.game.playerRightScore = self.playerRightScore
            self.game.finished_at = timezone.now()
            self.game.save()
        except:
            pass

    def end_game(self):
        try:
            print("Ending game")
            self.game.status = Game.GameStatus.FINISHED
            self.game.playerLeftScore = self.playerLeftScore
            self.game.playerRightScore = self.playerRightScore
            self.game.save()
        except:
            pass

class GameEngine(threading.Thread):

    playerCount = 0

    players = []

    def __init__(self, channel_name, **kwargs):
        super(GameEngine, self).__init__(daemon=True, name="GameEngine", **kwargs)
        self.group_name = "pong"
        self.channel_name = channel_name
        self.channel_layer = get_channel_layer()
        self.games = {}

    def run(self) -> None:
        while True:
            for game in list(self.games.values()):
                if game.status == game.GameStatus.PAUSED and game.disconnection_time:
                    if (timezone.now() - game.disconnection_time).seconds > 30:
                        game.game_winned_disconnected()
                if game.status != game.GameStatus.PLAYING:
                    continue

                self.update_ball_position(game.group_name)  # Update ball position
                self.broadcast_state(game.group_name, game.game_state)  # Broadcast game state
            time.sleep(0.016)

    def broadcast_state(self, group_name, game_state):
        async_to_sync(self.channel_layer.group_send)(
            group_name, {"type": "game_update", "game_dict": game_state}
        )

    def add_player(self, group_name, user_id, game_id, invite_id):
        if group_name not in self.games:
            self.games[group_name] = GameInstance(group_name)
        try:
            self.games[group_name].add_player(user_id, game_id, invite_id)
        except Exception as e:
            print("Error adding player: ", e)
            async_to_sync(self.channel_layer.group_send)(
                group_name, {"type": "game_update", "end_dict": {"error": "Error adding player"}}
            )
            self.games[group_name].end_game()
            self.games.pop(group_name)


    def remove_player(self, group_name, user_id):
        if group_name not in self.games:
            return
        try:
            self.games[group_name].remove_player(user_id)
        except Exception as e:
            print("Error removing player: ", e)
            async_to_sync(self.channel_layer.group_send)(
                group_name, {"type": "game_update", "end_dict": {"error": "Error removing player"}}
            )
            self.games[group_name].end_game()
            self.games.pop(group_name)

    def end_game(self, group_name):
        if group_name not in self.games:
            return
        self.games[group_name].end_game()
        self.games.pop(group_name)

    def restart_state(self, group_name):
        game = self.games[group_name]
        game.restart_state()

    def kick_dot(self, group_name):
        game = self.games[group_name]

        if not game.started and not game.dotKicked:
            game.restart_state()
            game.started = True
        elif game.started and not game.dotKicked:
            game.dotKicked = True 

    def update_ball_position(self, group_name):
        game = self.games[group_name]

        if not game.dotKicked:
            return
        # loosing because of coliision with the left wall
        if (game.dotX + game.speedX - 0.5) < 1:
            game.dotKicked = False
            game.started = False
            game.player_scored("right")
            async_to_sync(self.channel_layer.group_send)(
                game.group_name, {"type": "game_update", "score_dict": {"left":
                                                                        game.playerLeftScore,
                                                                        "right":
                                                                        game.playerRightScore}}
            )
        # loosing because of coliision with the right wall
        elif (game.dotX + game.speedX + 0.5) > 99:
            game.dotKicked = False
            game.started = False
            game.player_scored("left")
            async_to_sync(self.channel_layer.group_send)(
                game.group_name, {"type": "game_update", "score_dict": {"left": game.playerLeftScore, "right":
                                                                        game.playerRightScore}}
            )
        #bouncing at the top
        elif (game.dotY + game.speedY - 0.5) < 1:
            game.speedY = -game.speedY
            game.dotY += game.speedY
        # bouncing at the bottom
        elif (game.dotY + game.speedY + 0.5) > 99:
            game.speedY = -game.speedY
            game.dotY += game.speedY
        # bouncing at the right paddle
        elif (game.dotX + game.speedX + 0.5) > 93 and (game.paddle_right - 15) < game.dotY < (game.paddle_right + 15):
            game.speedX = -game.speedX
            game.dotX += game.speedX
        # bouncing at the left paddle
        elif (game.dotX + game.speedX - 0.5) < 7 and (game.paddle_left - 15) < game.dotY < (game.paddle_left + 15):
            game.speedX = -game.speedX
            game.dotX += game.speedX
        #regular movement
        else:
            game.dotY += game.speedY
            game.dotX += game.speedX
        game.game_state['ball'] = [game.dotX, game.dotY] 

    def update_paddle_position(self, player, action, group_name):
        game = self.games[group_name]
        if game.status != game.GameStatus.PLAYING:
            return
        player_side = game.player_side(player)
        if action == "W" or action == "UP":
            if game.game_state['paddle_'+player_side] - game.dx-15 < 1:
                return
            game.game_state['paddle_'+player_side] -= game.dx
        elif action == "S" or action == "DOWN":
            if game.game_state['paddle_'+player_side] + game.dx + 15 > 99:
                return
            game.game_state['paddle_'+player_side] += game.dx
        game.paddle_right = game.game_state['paddle_right']
        game.paddle_left = game.game_state['paddle_left']
