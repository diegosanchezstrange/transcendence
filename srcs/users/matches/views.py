from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated

from .models import Match
from django.db.models import Q

class MatchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Returns a list of matches of the user

        """
        user = request.user
        matches = Match.objects.filter(Q(user1=user) | Q(user2=user))

        response = []
        for match in matches:
            
            if match.player_1 == user:
                opponent = match.player_2
            else:
                opponent = match.player_1
            
            response.append(
                {
                    "date": match.date,
                    "opponent": opponent,
                    "winner": match.winner,
                }
            )

        return JsonResponse({
            "matches": matches
        })
