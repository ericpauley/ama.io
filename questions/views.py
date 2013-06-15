from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from questions.models import AMASession


def test(request):
    return render(request, "base.html")

def user(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404
    return render(request, "user.html", {'user': user})

def session(request, slug):
    try:
        s = AMASession.objects.get(slug=slug.lower())
    except AMASession.DoesNotExist:
        raise Http404
    return render(request, "session.html", {'session':s})
