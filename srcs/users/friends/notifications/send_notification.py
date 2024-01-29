from .constants import notification_messages
import json
import requests
from src.settings import MICROSERVICE_API_TOKEN, NOTIFICATIONS_SERVICE_HOST
import os


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
    response = requests.post(f"{NOTIFICATIONS_SERVICE_HOST}/notifications/send/", 
                             json=data,
                             headers={"Authorization": MICROSERVICE_API_TOKEN}, verify=False)

    print(json.dumps(response.json(), indent=2))
