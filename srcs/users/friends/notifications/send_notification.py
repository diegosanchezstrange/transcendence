from .constants import notification_messages
import json
import requests
from src.settings import MICROSERVICE_API_TOKEN


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
    # TODO: get hostname from environment

    # TODO: check if fails
    response = requests.post("http://localhost:8083/notifications/send/",
                             json=data,
                             headers={"Authorization": MICROSERVICE_API_TOKEN})

    print(json.dumps(response.json(), indent=2))
