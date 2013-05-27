from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.authorization import ReadOnlyAuthorization
from questions.models import AMASession,AMAQuestion,AMAAnswer
from questions.authorization import SessionAuthorization
from django.contrib.auth.models import User
from django.db.models import Sum

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'last_login']
        allowed_methods = ['get']
        authorization = ReadOnlyAuthorization()

class SessionResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')

    class Meta:
        queryset = AMASession.objects.all()
        resource_name = 'session'
        fields = ['owner', 'start_time', 'end_time']
        authorization = SessionAuthorization()

class QuestionResource(ModelResource):

    answer = fields.OneToOneField('questions.api.AnswerResource', 'answer', related_name='question', null=True)
    score = fields.IntegerField(attribute='score', default=0, readonly=True)

    class Meta:
        queryset = AMAQuestion.objects.all().annotate(score=Sum('votes__value'))
        resource_name = 'question'
        
class AnswerResource(ModelResource):
    question = fields.OneToOneField(QuestionResource, 'question', related_name='answer')

    class Meta:
        queryset = AMAAnswer.objects.all()
        resource_name = 'answer'