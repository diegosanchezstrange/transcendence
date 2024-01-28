from django.shortcuts import render

context = {}

def start(request):
    context['PATH'] = 'pong'
    auth = request.headers.get('Authorization')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'start.html', context)
    else:
        return render(request, '../templates/base.html', context)

# class LobbyView(TemplateView):
#     template_name = 'lobby.html'
 
#     def get_context_data(self, **kwargs):
#         context = super(LobbyView, self).get_context_data(**kwargs)
#         # get current open games to prepopulate the list
 
#         return context