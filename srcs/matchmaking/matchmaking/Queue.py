from .Notifier import Notifier
import requests

from django.conf import settings


class Queue:
    __queue = []

    class UserNotInQueueError(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__("The user is not currently in a queue.")

    @staticmethod
    def add_player(user):
        Queue.__queue.append(user)

        if Queue.is_match_ready():
            player2 = Queue.__queue.pop()
            player1 = Queue.__queue.pop()

            print(f"Match is ready: {player1.username} - {player2.username}")

            headers = {
                'Authorization': settings.MICROSERVICE_API_TOKEN,
                'Content-Type': 'application/json'
            }

            url = f'{settings.GAME_SERVICE_HOST_INTERNAL}/'

            body = {
                'playerLeft': player1.id,
                'playerRight': player2.id
            }

            response = requests.post(url, headers=headers, verify=False, json=body)
            response.raise_for_status()

            try:
                Notifier(player1=player1, player2=player2).send_msg_to_notifications_service()
            except Exception as e:
                print(e)
                print('Error while sending notification')



    @staticmethod
    def is_user_in_queue(user) -> bool:
        return user in Queue.__queue
    
    @staticmethod
    def leave_queue(user):
        if not Queue.is_user_in_queue(user=user):
            raise Queue.UserNotInQueueError()
        Queue.__queue.remove(user)

    @staticmethod
    def is_match_ready() -> bool:
        return len(Queue.__queue) == 2
    
    @staticmethod
    def get_queue():
        return Queue.__queue
    
    @staticmethod
    def delete_queue():
        Queue.__queue = []
