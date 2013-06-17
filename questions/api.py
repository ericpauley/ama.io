from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Sum
from questions.authorization import SessionAuthorization
from questions.models import AMASession,AMAQuestion,AMAAnswer,AMAVote
from tastypie import fields
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpConflict, HttpBadRequest, HttpApplicationError
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
import json
from markdown import markdown

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'last_login']
        allowed_methods = ['get']
        authorization = ReadOnlyAuthorization()
        filtering = {
            'first_name': ALL,
            'last_name': ALL,
            'username': ALL

        }
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
            url(r'^(?P<resource_name>%s)/register%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('register'), name='api_register'),
        ]

    def register(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        username = request.POST.get('username', '').lower()
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm', '')

        if password != confirm:
            return self.create_response(request, {
                    'success': False,
                    'reason': 'pass_match',
                }, HttpBadRequest)

        if User.objects.filter(username=username).count() > 0:
            return self.create_response(request, {
                    'success': False,
                    'reason': 'exists',
                }, HttpConflict)

        user = User.objects.create_user(username, email, password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True
                })
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'error',
                }, HttpApplicaitonError )


    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
                }, HttpUnauthorized )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)

class SessionResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')
    questions = fields.ToManyField('questions.api.QuestionResource', lambda bundle:bundle.obj.get_marked_questions(bundle.request.user), use_in='detail', full='true', related_name='session')

    class Meta:
        queryset = AMASession.objects.all()
        resource_name = 'session'
        authorization = SessionAuthorization()
        filtering = {
            'owner': ALL_WITH_RELATIONS,
            'start_time': ALL,
            'end_time': ALL
        }

    def dehydrate_data(self, bundle):
        if 'desc' in bundle.obj.data:
            bundle.obj.data['desc-html'] = markdown(bundle.obj.data['desc'])
        return bundle.obj.data

class QuestionResource(ModelResource):

    answer = fields.OneToOneField('questions.api.AnswerResource', 'answer', related_name='question', null=True, full=True)
    session = fields.OneToOneField('questions.api.SessionResource', 'session', null=True)
    score = fields.IntegerField(attribute='score', default=0, readonly=True)

    class Meta:
        queryset = AMAQuestion.objects.all().annotate(_score=Sum('votes__value'))
        resource_name = 'question'
        filtering = {
            'session': ALL_WITH_RELATIONS,
            'answer': ALL_WITH_RELATIONS,
            'score': ALL
        }

    def dehydrate(self, bundle):
        bundle.data['vote'] = bundle.obj.vote
        return bundle

    def get_object_list(self, request):
        if request.user.is_authenticated():
            return super(QuestionResource, self).get_object_list(request).extra(select = {
                    "_vote" : """
                    SELECT value
                    FROM questions_amavote
                    WHERE questions_amavote.question_id = questions_amaquestion.id
                    AND questions_amavote.user_id = (%d)
                    """ % request.user.id
                })
        else:
            return super(QuestionResource, self).get_object_list(request)

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/vote%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('vote'), name="api_login"),
        ]

    def vote(self, request, pk, **kwargs):
        self.method_check(request, allowed=['post'])

        if not request.user.is_authenticated():
            return self.create_response(request, {
                'success': False,
                'reason': 'not_logged_in',
                }, HttpUnauthorized )

        if AMAQuestion.objects.filter(pk=pk).count() == 0:
            return self.create_response(request, {
                'success': False,
                'reason': 'no_question',
                }, HttpBadRequest )

        vote = int(request.POST.get('vote', 0))
        if not vote in (-1,0,1):
            return self.create_response(request, {
                'success': False,
                'reason': 'bad_vote',
                }, HttpBadRequest )

        AMAVote.objects.filter(question__pk=pk, user__username=request.user.username).delete()
        if vote != 0:
            AMAVote(user=request.user, question=AMAQuestion.objects.get(pk=pk), value=vote).save()
        return self.create_response(request, {
            'success': True,
            'score': AMAQuestion.objects.all().annotate(_score=Sum('votes__value')).get(pk=pk).score
        })

class AnswerResource(ModelResource):
    question = fields.OneToOneField(QuestionResource, 'question', related_name='answer')

    class Meta:
        queryset = AMAAnswer.objects.all()
        resource_name = 'answer'
