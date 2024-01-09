from enum import Enum


class NotificationType(Enum):
    SENT = 1
    ACCEPTED = 2
    REJECTED = 3


notification_messages = {
    NotificationType.SENT: " has sent you a friend request.",
    NotificationType.ACCEPTED: " has accepted your friend request.",
    NotificationType.REJECTED: " has rejected your friend request."
}
