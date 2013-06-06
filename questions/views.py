# Create your views here.
from django.http import Http404
from django.shortcuts import render

from questions.models import Session

def test(request):
    return render(request, "body.html")
    
def session(request, slug):
    try:
        s = session.objects.get(slug=slug.lower())
    except Session.DoesNotExist:
        raise Http404
    return render(request, "session.html", {'session':s})