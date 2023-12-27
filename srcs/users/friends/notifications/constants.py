from enum import Enum


class NotificationType(Enum):
    SENT = 1
    ACCEPTED = 2


notification_messages = {
    NotificationType.SENT: " has sent you a friend request.",
    NotificationType.ACCEPTED: " has accepted your friend request."
}
