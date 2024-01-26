from django.shortcuts import render

context = {}

def start(request):
    context['PATH'] = 'pong'
    return render(request, 'start.html', context)

# class LobbyView(TemplateView):
#     template_name = 'lobby.html'
 
#     def get_context_data(self, **kwargs):
#         context = super(LobbyView, self).get_context_data(**kwargs)
#         # get current open games to prepopulate the list
 
#         return context