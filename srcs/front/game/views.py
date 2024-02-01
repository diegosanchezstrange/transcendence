from django.shortcuts import render
from django.views.decorators.cache import never_cache

context = {}

@never_cache
def start(request):
    context['PATH'] = 'pong'
    auth = request.headers.get('Authorization')
    # TO DO: request game info from database
    context['game_info'] = {
        "player_1": "Player 1",
        "player_2": "Player 2",
        "score_1": "0",
        "score_2": "0"
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'start.html', context)
    else:
        return render(request, '../templates/base.html', context)

@never_cache
def lobby(request):
    context['PATH'] = 'lobby'
    # TO DO: request game info from database
    context['waitlist'] = [
        "Player 3",
        "Player 4",
        "Player 5"
    ]
    context['game_ongoing'] = True
    context['player_1'] = "Bob"
    context['player_2'] = "Ross"
    auth = request.headers.get('Authorization')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'lobby.html', context)
    else:
        return render(request, '../templates/base.html', context)

# class LobbyView(TemplateView):
#     template_name = 'lobby.html'
 
#     def get_context_data(self, **kwargs):
#         context = super(LobbyView, self).get_context_data(**kwargs)
#         # get current open games to prepopulate the list
 
#         return context