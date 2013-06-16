from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render
from questions.models import AMASession


def home(request):
    sessions = AMASession.objects.all().extra(order_by = ['-start_time'])
    return render(request, "home.html", {'sessions': sessions})

def user(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404
    return render(request, "user.html", {'user': user})

def session(request, slug):
    try:
        s = AMASession.objects.get(slug=slug.lower())
        answered = s.get_marked_questions(request.user).exclude(answer=None)
        unanswered = s.get_marked_questions(request.user).filter(answer=None)
    except AMASession.DoesNotExist:
        raise Http404
    return render(request, "session.html", {'session':s, 'unanswered': unanswered, 'answered': answered})
