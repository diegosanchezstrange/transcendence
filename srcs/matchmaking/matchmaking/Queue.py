from .Notifier import Notifier


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

            Notifier(player1=player1, player2=player2).send_msg_to_notifications_service()

    @staticmethod
    def is_user_in_queue(user) -> bool:
        return user in Queue.__queue
    
    @staticmethod
    def remove_user_from_queue(user):
        if Queue.is_user_in_queue(user=user):
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