from django.conf.urls import patterns, include, url
from tastypie.api import Api
from questions.api import UserResource, SessionResource, QuestionResource, AnswerResource
from questions import views

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(SessionResource())
v1_api.register(QuestionResource())
v1_api.register(AnswerResource())

urlpatterns = patterns('',
    url(r'^$', views.test),
    url(r'^api/', include(v1_api.urls)),
)
