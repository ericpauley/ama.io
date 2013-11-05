from questions.models import Request, AMASession
from allauth.socialaccount import providers
from django.utils import timezone
from questions.api import UserResource

processors = []

def process(function):
	processors.append(function)

def run_processors(request):
	env = {}
	for function in processors:
		env.update(function(request))
	return env

@process
def my_live_sessions(request):
	if request.user.is_authenticated():
		return {"my_live_sessions": request.user.sessions.filter(
        start_time__lt=timezone.now(),
        end_time__gt=timezone.now())[:1]}
	else:
		return {}

@process
def live_sessions(request):
	return {'live_sessions': AMASession.objects.live()[:9]}

@process
def oauth_providers(request):
	return {"oauth_providers": providers.registry.as_choices()}

@process
def has_requests(request):
	if request.user.is_authenticated():
		return {"num_requests": Request.objects.for_user(request.user).filter(session=None).count()}
	else:
		return {}

@process
def now(request):
	return {"now": timezone.now()}
