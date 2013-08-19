from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render,redirect
from questions.models import AMASession, Request
from datetime import datetime

def live(request):
    live_sessions = AMASession.objects.all().filter(
        start_time__lt=datetime.now(),
        end_time__gt=datetime.now()).order_by('-start_time')
    return render(request, "session_list.html", {'sessions': live_sessions, 'title':'Live Sessions'})

def upcoming(request):
    upcoming_sessions = AMASession.objects.all().filter(
        start_time__gt=datetime.now()).order_by('-start_time')
    return render(request, "session_list.html", {'sessions': upcoming_sessions, 'title':'Upcoming Sessions'})

def home(request):
    live_sessions = AMASession.objects.all().filter(
        start_time__lt=datetime.now(),
        end_time__gt=datetime.now()).order_by('-start_time')[:15]
    upcoming_sessions = AMASession.objects.all().filter(
        start_time__gt=datetime.now()).order_by('-start_time')[:15]
    top_requests = Request.objects.all()[:15]
    return render(request, "home.html", {'live_sessions': live_sessions, 'upcoming_sessions': upcoming_sessions, 'top_requests': top_requests, 'title':'AMA'})

def user(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404
    return render(request, "user.html", {'user': user})

def user_sessions(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404
    return render(request, "session_list.html", {'sessions': user.sessions.order_by("-start_time"), 'title':"%s's Sessions" % username})

def session(request, slug):
    try:
        s = AMASession.objects.get(slug=slug.lower())
        answered = s.get_marked_questions(request.user).exclude(answer=None)
        unanswered = s.get_marked_questions(request.user).filter(answer=None)
    except AMASession.DoesNotExist:
        raise Http404
    return render(request, "session.html", {'session':s, 'unanswered': unanswered, 'answered': answered})

def settings(request):
    if request.user.is_anonymous():
        return redirect("home")
    else:
        return render(request, "settings.html")

def settings_submit(request):
    pass
