from django.shortcuts import render

# Create your views here.
def start(request):
    return render(request, 'start.html')

# class LobbyView(TemplateView):
#     template_name = 'lobby.html'
 
#     def get_context_data(self, **kwargs):
#         context = super(LobbyView, self).get_context_data(**kwargs)
#         # get current open games to prepopulate the list
 
#         return context