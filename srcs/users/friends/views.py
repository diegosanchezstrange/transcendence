from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.db.models import Q
from .models import Friendship, FriendRequest
from .notifications.send_notification import send_friend_request_notification
from .notifications.constants import NotificationType
from .utils.utils import is_your_friend
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from functools import wraps
from django.utils.decorators import method_decorator

from django.conf import settings

def private_or_public_endpoint(f):
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return f(request, *args, **kwargs)
        
        api_token = request.headers.get('Authorization')
        if not api_token or api_token != settings.MICROSERVICE_API_TOKEN:
            return JsonResponse({'detail': 'Invalid API token.'}, status=401)
        return f(request, *args, **kwargs)
    return decorated_function

class FriendView(APIView):

    @method_decorator(permission_classes([]))
    @method_decorator(authentication_classes([]))
    @method_decorator(private_or_public_endpoint)
    def get(self, request, id=None):
        """
        Returns a list of friends of the user

        """
        if id:
            user = get_object_or_404(User, id=id)
        elif request.user.is_authenticated:
            user = request.user
        else:
            return JsonResponse({
                "detail": "User is not authenticated"
            }, status=401)

        print(user)

        friends = Friendship.objects.filter(Q(user1=user) | Q(user2=user))
        print(user.userprofile)


        users = []
        for friend in friends:
            if friend.user1 == user:
                users.append({
                    "username": friend.user2.username,
                    "id": friend.user2.id,
                    "is_online": friend.user2.userprofile.is_online,
                })
            elif friend.user2 == user:
                users.append({
                    "username": friend.user1.username,
                    "id": friend.user1.id,
                    "is_online": friend.user1.userprofile.is_online,
                })

        return JsonResponse({
            "users": users
        })


    @method_decorator(permission_classes([IsAuthenticated]))
    def delete(self, request, id=None):
        """
        Removes a friend from your friend list

        """
        sender = request.user
        receiver_id = request.data.get("friend_id")

        if not receiver_id:
            return JsonResponse({
                "detail": "No id provided"
            }, status=404)

        try:
            receiver = User.objects.get(id=receiver_id)
        except:
            return JsonResponse({
                "detail": "Receiver does not exist"
            }, status=404)

        friendship = get_object_or_404(Friendship, Q(user1=sender, user2=receiver) | Q(user1=receiver, user2=sender))

        friendship.delete()

        try:
            send_friend_request_notification(
                sender=sender,
                receiver=receiver,
                ntype=NotificationType.REMOVED
            )
        except:
            # TODO: Exception handling
            pass

        return JsonResponse({
            "detail": "Friend removed successfully"
        }, status=201)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, *args, **kwargs):
    """
    Sends a friend request to a user

    """
    send_to = request.data.get('send_to')
    if not send_to:
        return JsonResponse({
            "detail": "No value provided"
        }, status=400)

    receiver = get_object_or_404(User, username=send_to)

    if is_your_friend(request.user, receiver) or receiver == request.user:
        return JsonResponse({
            "detail": f"You are already a friend of {receiver.username}."
        }, status=409)

    friend_request, created = FriendRequest.objects.get_or_create(
        sender=request.user,
        receiver=receiver
    )
    if created:
        try:
            send_friend_request_notification(request.user, receiver, NotificationType.SENT)
        except Exception as e:
            #TODO: Exception handling
            print(e)
            pass

        return JsonResponse({
            "detail": "Friend request sent successfully"
        }, status=201)
    else:
        # TODO: send 304 (postman bug)
        return JsonResponse({
            "detail": "Friend request already sent."
        }, status=409)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_requests_list(request):
    """
    Returns a list of friend requests of the user
    """
    friend_requests = FriendRequest.objects.filter(receiver=request.user)

    result = [{"username": friend_request.sender.username, "id": friend_request.sender.id} for friend_request in friend_requests if friend_request]

    return JsonResponse({
        "users": result
    })




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, *args, **kwargs):
    """
    Accepts a friend request

    """
    receiver = request.user
    sender_id = request.data.get("sender")

    if not sender_id:
        return JsonResponse({
            "detail": "No id provided"
        }, status=400)

    try:
        sender = User.objects.get(id=sender_id)
    except:
        return JsonResponse({
            "detail": "Sender does not exist"
        }, status=404)

    friend_request = get_object_or_404(FriendRequest, sender=sender, receiver=receiver)


    friend_request.delete()
    Friendship.objects.create(user1=request.user, user2=friend_request.sender)

    try:
        send_friend_request_notification(
            sender=friend_request.receiver,
            receiver=friend_request.sender,
            ntype=NotificationType.ACCEPTED
        )
    except:
        #TODO: Exception handling
        pass

    return JsonResponse({
        "detail": "OK"
    }, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, *args, **kwargs):
    """
    Rejects a friend request

    """
    receiver = request.user
    sender_id = request.data.get("sender")

    if not sender_id:
        return JsonResponse({
            "detail": "No id provided"
        }, status=400)

    try:
        sender = User.objects.get(id=sender_id)
    except:
        return JsonResponse({
            "detail": "Sender does not exist"
        }, status=404)

    friend_request = get_object_or_404(FriendRequest, sender=sender, receiver=receiver)

    friend_request.delete()

    try:
        send_friend_request_notification(
            sender=friend_request.receiver,
            receiver=friend_request.sender,
            ntype=NotificationType.REJECTED
        )
    except:
        # TODO: Exception handling
        pass

    return JsonResponse({
        "detail": "Friend request rejected successfully"
    }, status=201)


