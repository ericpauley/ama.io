from django.conf.urls import patterns, include, url
from tastypie.api import Api
from questions.api import *
from questions import views
from django.views.decorators.cache import cache_page

class CachedApi(Api):
    def wrap_view(self, view):
        return cache_page(Api.wrap_view(self, view),10)
v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(SessionResource())
v1_api.register(QuestionResource())
v1_api.register(AnswerResource())
v1_api.register(RequestResource())
v1_api.register(CommentResource())

urlpatterns = patterns('',
    url(r'^$', views.home, name="home"),
    url(r'^live/$', views.live, name="live"),
    url(r'^upcoming/$', views.upcoming, name="upcoming"),
    url(r'^past/$', views.past, name="past"),
    url(r'^requests/$', views.requests, name="requests"),
    url(r'^requests/(?P<page>\d{1,5})/$', views.requests, name="requests"),
    url(r'^s/(?P<slug>\w{4})/$', views.session, name="session"),
    url(r'^u/(?P<username>[\w\-]{3,})/$', views.user, name="user"),
    url(r'^u/(?P<username>[\w\-]{3,})/sessions/$', views.user_sessions, name="user_sessions"),
    url(r'^q/(?P<question>\d{1,5})', views.question, name="question"),
    url(r'^settings/', views.settings),
    url(r'^settings/submit/', views.settings_submit),
    url(r'^api/', include(v1_api.urls)),

    #Static pages
    url(r'about/', views.static_page("2/about.html", "About"), name="about"),
    url(r'demo/', views.static_page("session-demo.html", "Session Tutorial"), name="demo")
)
