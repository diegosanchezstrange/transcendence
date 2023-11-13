from django.shortcuts import render
from django.utils.translation import gettext as _

def index(request):
    translated_text = _("text is test")
    return render(request, 'home.html', { 'test':  translated_text })
