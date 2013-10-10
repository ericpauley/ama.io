from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render,redirect
from questions.models import AMASession, Request, AMAQuestion, AMAVote
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib import messages
from json import dumps

def live(request):
    return render(request, "session_list.html", {'sessions': AMASession.objects.live()[:50], 'title':'Live Sessions'})

def past(request):
    return render(request, "session_list.html", {'sessions': AMASession.objects.past()[:50], 'title':'Past Sessions'})

def upcoming(request):
    return render(request, "session_list.html", {'sessions': AMASession.objects.upcoming()[:50], 'title':'Upcoming Sessions'})

def home(request):
    top_requests = Request.objects.all()[:5]
    return render(request, "2/home.html", {
        'live_sessions': AMASession.objects.live()[:6],
#        'upcoming_sessions': AMASession.objects.upcoming()[:6],
#        'past_sessions': AMASession.objects.past()[:6],
        'top_requests': top_requests,
        'title':'AMA'
    })

def question(request, question):
    try:
        question = AMAQuestion.objects.get(id=question)
    except AMAQuestion.DoesNotExist:
        raise Http404
    return render(request, "question_page.html", {"question": question})

def requests(request, page="1"):
    page = int(page)
    num = Request.objects.all().count()
    if (num <= (page-1)*20 and page != 1) or page == 0:
        return redirect("requests",page=1)
    prev = None if page == 1 else reverse("requests", kwargs={"page":page-1})
    next = None if 20*page >= num else reverse("requests", kwargs={"page":page+1})
    top_requests = top_requests = Request.objects.all()[(page-1)*20:page*20]
    title = "Requests"
    return render(request, "request_list.html", locals())

def user(request, username):
    try:
        user = User.objects.get(username=username.lower())
    except User.DoesNotExist:
        raise Http404
    past = AMASession.objects.past().filter(owner=user)[:4]
    upcoming = AMASession.objects.upcoming().filter(owner=user)[:4]
    live = AMASession.objects.live().filter(owner=user)[:1]
    return render(request, "user.html", {'user': user, 'past':past, 'upcoming':upcoming, 'live':live})

def user_sessions(request, username):
    try:
        user = User.objects.get(username=username.lower())
    except User.DoesNotExist:
        raise Http404
    return render(request, "session_list.html", {'sessions': user.sessions.order_by("-start_time"), 'title':"%s's Sessions" % username})

def session(request, slug):
    try:
        s = AMASession.objects.get(slug=slug.lower())
        s.mark_viewed(request)
        answered = s.get_marked_questions(request).exclude(answer=None)
        unanswered = s.get_marked_questions(request).filter(answer=None)
        if request.user.is_authenticated():
            votes = dumps(dict([(str(vote.question_id),vote.value) for vote in request.user.votes.filter(question__session=s)]))
        else:
            votes = None
        if not s.owner.meta.is_verified:
            if s.owner == request.user:
                messages.add_message(request, messages.WARNING, 'You have not yet linked a verified Twitter account. You can do so <a href="/accounts/twitter/login/?process=connect">here</a>.')
            else:
                messages.add_message(request, messages.WARNING, 'This user has not verified their account with Twitter. Beware of impersonators.')
    except AMASession.DoesNotExist:
        raise Http404
    return render(request, "2/session_page.html", {'session':s, 'unanswered': unanswered, 'answered': answered, 'votes':votes})

def settings(request):
    if request.user.is_anonymous():
        return redirect("home")
    else:
        return render(request, "settings.html")

def static_page(page, title):
    return lambda request: render(request, page, {"title": title})

def settings_submit(request):
    pass
