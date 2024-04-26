from .Notifier import Notifier
import requests

from django.conf import settings

class Tournament:
    __queue = []
    __ongoing_matches = []

    tournament_size = 4

    class UserNotInQueueError(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__("The user is not currently in a queue.")

    @staticmethod
    def add_player(user):
        Tournament.__queue.append(user)
        # Add UserTournament?
        print(f"Player {user.username} has joined the tournament")

        print(f"Current tournament: {[p.username for p in Tournament.__queue]}")

        if Tournament.is_match_ready():
            players = [Tournament.__queue.pop() for i in range(Tournament.tournament_size)]

            for p in players:
                print(f"Match is ready: {p.username}")

            headers = {
                'Authorization': settings.MICROSERVICE_API_TOKEN,
                'Content-Type': 'application/json'
            }

            body = {"players": []}
            
            for i, player in enumerate(players):
                body["players"].append({"id": player.id})

            response = requests.post(f'{settings.GAME_SERVICE_HOST_INTERNAL}/tournament/', headers=headers, verify=False, json=body)
            response.raise_for_status()

            try:
                Notifier().send_msg_to_tournament_players(users=players,
                                                          tournament_id=response.json()['tournament_id'])
            except Exception as e:
                print(e)
                print('Error while sending notification')

    @staticmethod
    def is_user_in_queue(user) -> bool:
        return user in Tournament.__queue

    @staticmethod
    def leave_queue(user):
        if Tournament.is_user_in_queue(user=user):
            raise Tournament.UserNotInQueueError()
        Tournament.__queue.remove(user)

    @staticmethod
    def is_match_ready() -> bool:
        return len(Tournament.__queue) == Tournament.tournament_size

