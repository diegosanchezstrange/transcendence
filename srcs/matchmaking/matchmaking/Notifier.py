import requests
from django.conf import settings


class Notifier:
    def __init__(self, player1, player2) -> None:
        self.player1 = player1
        self.player2 = player2

    @staticmethod
    def __construct_data(player1, player2) -> dict:
        data = {
            "message":
            {
                "message": f"Match found against player: {player2.username}",
                "ntype": 11,
                "sender": {
                    "id": player2.id,
                    "username": player2.username
                },
                "receiver": {
                    "id": player1.id,
                    "username": player1.username
                },

            }
        }
        return data
    def __construct_tournament_data(self, user, users) -> dict:
        data = {
            "message":
            {
                "message": f"Match found against player: {user.username}",
                "ntype": 11,
                "receiver": {
                    "id": user.id,
                    "username": user.username
                },
                "players": []

            }
        }
        for u in users:
            data["message"]["players"].append({
                "id": u.id,
                "username": u.username
            })

        return data
    
    def send_msg_to_notifications_service(self):

        print(f"Sending notification to {self.player1.username} and {self.player2.username}")
        print(f"{settings.NOTIFICATIONS_SERVICE_HOST_INTERNAL}/notifications/send/")

        requests.post(
            f"{settings.NOTIFICATIONS_SERVICE_HOST_INTERNAL}/notifications/send/",
            verify=False,
            headers={"Authorization": settings.MICROSERVICE_API_TOKEN},
            json=Notifier.__construct_data(self.player1, self.player2)
        )

        requests.post(
            f"{settings.NOTIFICATIONS_SERVICE_HOST_INTERNAL}/notifications/send/",
            verify=False,
            headers={"Authorization": settings.MICROSERVICE_API_TOKEN},
            json=Notifier.__construct_data(self.player2, self.player1)
        )
    def send_msg_to_tournament_players(self, users):
        for user in users:
            print(f"Sending notification to {user.username}")
            print(f"{settings.NOTIFICATIONS_SERVICE_HOST_INTERNAL}/notifications/send/")

            requests.post(
                f"{settings.NOTIFICATIONS_SERVICE_HOST_INTERNAL}/notifications/send/",
                verify=False,
                headers={"Authorization": settings.MICROSERVICE_API_TOKEN},
                json=Notifier.__construct_data(user, users)
            )
