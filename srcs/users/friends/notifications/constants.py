from enum import Enum


class NotificationType(Enum):
    SENT = 1
    ACCEPTED = 2
    REJECTED = 3
    REMOVED = 4
    NAME_CHANGED = 5
    IMG_CHANGED = 6
    USER_ONLINE = 7
    USER_OFFLINE = 8
    USER_ONLINE_NOTIFICATION = 9
    USER_OFFLINE_NOTIFICATION = 10
    GAME_FOUND = 11
    GAME_INVITE = 12


notification_messages = {
    NotificationType.SENT: " has sent you a friend request.",
    NotificationType.ACCEPTED: " has accepted your friend request.",
    NotificationType.REJECTED: " has rejected your friend request.",
    NotificationType.REMOVED: " has removed you from their friends list.",
    NotificationType.NAME_CHANGED: "",
    NotificationType.IMG_CHANGED: "",
    NotificationType.USER_ONLINE: "",
    NotificationType.USER_OFFLINE: "",
    NotificationType.USER_ONLINE_NOTIFICATION: "",
    NotificationType.USER_OFFLINE_NOTIFICATION: "",
    NotificationType.GAME_FOUND: "Match found against player: ",
    NotificationType.GAME_INVITE: " has invited you to a game."
}
