from allaccess.models import Provider

def recent_sessions(request):
	if request.user.is_authenticated():
		return {"recent_sessions": request.user.sessions.order_by("-start_time")[:5]}
	else:
		return {}

def oauth_providers(request):
	return {"oauth_providers": Provider.objects.order_by("name")}
