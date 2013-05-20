from django.conf.urls import patterns, include, url
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'sessions', views.SessionViewSet)
router.register(r'questions', views.QuestionViewSet)

urlpatterns = patterns('',
	url(r'^', include(router.urls)),
    url(r'^', include('rest_framework.urls', namespace='rest_framework'))
)
