from django.conf.urls import patterns, include, url
from tastypie.api import Api
from questions.api import *
from questions import views

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(SessionResource())
v1_api.register(QuestionResource())
v1_api.register(AnswerResource())
v1_api.register(RequestResource())

urlpatterns = patterns('',
    url(r'^$', views.home),
    url(r'^live/$', views.live, name="live"),
    url(r'^upcoming/$', views.upcoming, name="upcoming"),
    url(r'^requests/$', views.requests, name="requests"),
    url(r'^s/(?P<slug>\w{4})/$', views.session, name="session"),
    url(r'^session/(?P<slug>\w{4})/$', views.session),
    url(r'^u/(?P<username>\w{4,})/$', views.user, name="user"),
    url(r'^u/(?P<username>\w{4,})/sessions/$', views.user_sessions, name="user_sessions"),
    url(r'^user/(?P<username>\w{4,})/$', views.user),
    url(r'^user/(?P<username>\w{4,})/sessions/$', views.user_sessions),
    url(r'^settings/', views.settings),
    url(r'^settings/submit/', views.settings_submit),
    url(r'^api/', include(v1_api.urls)),

    #Static pages
    url(r'about/', views.static_page("about.html", "About"))
)
