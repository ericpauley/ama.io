from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import viewsets

from api.serializers import UserSerializer, SessionSerializer, QuestionSerializer
from questions.models import AMASession, AMAQuestion

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SessionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = AMASession.objects.all()
    serializer_class = SessionSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = AMAQuestion.objects.all().annotate(score=Sum('votes'))
    serializer_class = QuestionSerializer
