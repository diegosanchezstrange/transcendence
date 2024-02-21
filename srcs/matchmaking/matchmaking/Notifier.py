import requests
from .settings import NOTIFICATIONS_SOCKETS_HOST_INTERNAL, MICROSERVICE_API_TOKEN


class Notifier:
    def __init__(self, player1, player2) -> None:
        self.player1 = player1
        self.player2 = player2

    @staticmethod
    def __construct_data(player1, player2) -> dict:
        data = {
            "receiver": {
                "id": player1.id,
                "username": player1.username
            },
            "message": f"Match found against player: {player2.username}"
        }
        return data
    
    def send_msg_to_notifications_service(self):

        requests.post(
            f"{NOTIFICATIONS_SOCKETS_HOST_INTERNAL}/notifications/send/",
            headers={"Authorization": MICROSERVICE_API_TOKEN},
            json=Notifier.__construct_data(self.player1, self.player2)
        )

        requests.post(
            f"{NOTIFICATIONS_SOCKETS_HOST_INTERNAL}/notifications/send/",
            headers={"Authorization": MICROSERVICE_API_TOKEN},
            json=Notifier.__construct_data(self.player2, self.player1)
        )
