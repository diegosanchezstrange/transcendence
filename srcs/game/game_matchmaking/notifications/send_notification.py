from .constants import notification_messages
import json
import requests
from django.conf import settings
from game_matchmaking.models import Tournament, UserTournament


def send_friend_request_notification(sender, receiver, ntype):
    data = {
        "sender": {
            "id": sender.id,
            "username": sender.username
        },
        "receiver": {
            "id": receiver.id,
            "username": receiver.username
        },
        "message": f"{sender.username} {notification_messages[ntype]}"
    }

    # print(json.dumps(data, indent=2))

    # TODO: check if fails
    response = requests.post(f"{settings.NOTIFICATIONS_SERVICE_HOST_INTERNAL}/notifications/send/", 
                             json=data,
                             headers={"Authorization": settings.MICROSERVICE_API_TOKEN}, verify=False)

    print(json.dumps(response.json(), indent=2))

def send_tournament_players_update_notification(tournament):
    tournament_players = UserTournament.objects.filter(tournament=tournament)

    print(tournament_players)

    for player in tournament_players:
        print("Sending notification to: ", player.user.username)
        data = {
            "receiver": {
                "id": player.user.id,
                "username": player.user.username
            },
            "ntype": 14,
            "tournament_id": tournament.id,
            "message": f"Tournament new match"
        }

        # print(json.dumps(data, indent=2))
        response = requests.post(f"{settings.NOTIFICATIONS_SERVICE_HOST_INTERNAL}/notifications/send/",
                                 json=data,
                                 headers={"Authorization": settings.MICROSERVICE_API_TOKEN}, verify=False)

