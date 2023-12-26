from django.db.models import Q
from ..models import Friendship


def is_your_friend(user1, user2):
    return Friendship.objects.filter(
        (Q(user1=user1) & Q(user2=user2)) |
        (Q(user1=user2) & Q(user2=user1))
    ).exists()
