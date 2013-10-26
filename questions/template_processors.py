from questions.models import Request
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
def recent_sessions(request):
	if request.user.is_authenticated():
		return {"recent_sessions": request.user.sessions.order_by("-start_time")[:5]}
	else:
		return {}

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
