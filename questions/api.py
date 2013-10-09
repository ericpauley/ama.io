import json

from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Sum
from django.template.loader import render_to_string
from django.shortcuts import render
from markdown import markdown
from questions.authorization import *
from questions.models import *
from questions.forms import *
from tastypie import fields
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.http import HttpUnauthorized, HttpForbidden, HttpConflict, HttpBadRequest, HttpApplicationError, HttpNotFound
from tastypie.resources import ModelResource, Resource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from django.template import RequestContext
from dateutil import parser
import datetime
import re
import json
from tastypie.cache import NoCache, SimpleCache
from django.db import transaction
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from allauth.socialaccount import providers
from django.shortcuts import get_object_or_404
from tastypie.validation import *
from django.views.decorators.cache import cache_page
from django.core.files.images import get_image_dimensions
import hashlib
import base64
import sys
import traceback
from easy_thumbnails.files import get_thumbnailer
import allauth.account.utils
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp
from django.utils import timezone
from allauth.socialaccount.providers.oauth.client import OAuth

class CachedResource():
    def wrap_view(self, view):
        return cache_page(Resource.wrap_view(self, view),10)

class UserResource(ModelResource):
    display = fields.CharField(readonly = True)

    def dehydrate_display(self, bundle):
        return bundle.obj.meta.full_name

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
            url(r'^(?P<resource_name>%s)/make_old%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('make_old'), name='api_make_old'),
            url(r'^(?P<resource_name>%s)/make_new%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('make_new'), name='api_make_new'),
        ]

    def register(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        username = request.POST.get('username', '').lower()
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm', '')

        if not re.match(r"^\w{4,30}$", username):
            return self.create_response(request, {
                    'success': False,
                    'reason': 'bad_username',
                }, HttpBadRequest)

        if not re.match(r"^.{6,50}$", password):
            return self.create_response(request, {
                    'success': False,
                    'reason': 'bad_password',
                }, HttpBadRequest)

        try:
            validate_email(email)
        except ValidationError:
            return self.create_response(request, {
                    'success': False,
                    'reason': 'bad_email',
                }, HttpBadRequest)

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
        if EmailAddress.objects.filter(email__iexact=email).exists():
            return self.create_response(request, {
                    'success': False,
                    'reason': 'email_exists',
                }, HttpConflict)

        if username+"\n" in open("reserved.txt").readlines():
            return self.create_response(request, {
                    'success': False,
                    'reason': 'reserved',
                }, HttpConflict)

        user = User.objects.create_user(username, email, password)
        allauth.account.utils.setup_user_email(request, user, [EmailAddress(
                                                                    email=email,
                                                                    primary=True,
                                                                    verified=False)])
        allauth.account.utils.send_email_confirmation(request, user, True)
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return self.create_response(request, {
                'success': True
            })
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'error',
                }, HttpApplicationError )


    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        username = request.POST.get('username', '').lower()
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        allauth.account.utils.sync_user_email_addresses(user)
        allauth.account.utils.send_email_confirmation(request, user)
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
        
    def make_old(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        username = request.POST.get('username', '').lower()
        user = User.objects.filter(username=username)
        if user.count() == 0:
            return self.create_response(request, { 'success': False }, HttpNotFound)
        elif user.count() == 1 and request.user and request.user.is_authenticated():
            user = user[0]
            #print "User was "+str(user.meta.new)
            user.meta.new = False
            #print "User is now "+str(user.meta.new)
            user.meta.save()
            user.save()
            #print "User is now "+str(user.meta.new)
            return self.create_response(request, { 'success': True})
        return self.create_response(request, { 'success': False, 'reason': "Dup User"}, HttpNotFound)
    
    def make_new(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        username = request.POST.get('username', '').lower()
        user = User.objects.filter(username=username)
        if user.count() == 0:
            return self.create_response(request, { 'success': False }, HttpNotFound)
        elif user.count() == 1 and request.user and request.user.is_authenticated():
            user = user[0]
            #print "User was "+str(user.meta.new)
            user.meta.new = True
            #print "User is now "+str(user.meta.new)
            user.meta.save()
            user.save()
            #print "User is now "+str(user.meta.new)
            return self.create_response(request, { 'success': True})
        return self.create_response(request, { 'success': False, 'reason': "Dup User"}, HttpNotFound)
    

class SessionResource(CachedResource, ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner', readonly=True)
    questions = fields.ToManyField('questions.api.QuestionResource', readonly=True, attribute='questions', null=True, use_in='detail', full=True, related_name='session')
    num_viewers = fields.IntegerField(attribute="num_viewers", readonly=True)
    time = fields.DateField()
    image = fields.CharField(attribute="auto_image", readonly=True)
    state = fields.CharField(attribute="state", readonly=True)

    def dehydrate_time(self, bundle):
        return timezone.now()

    class Meta:
        queryset = AMASession.objects.all()
        resource_name = 'session'
        authorization = SessionAuthorization()
        filtering = {
            'owner': ALL_WITH_RELATIONS,
            'start_time': ALL,
            'end_time': ALL
        }
        validation = FormValidation(form_class=SessionForm)

    def dehydrate(self, bundle):
        bundle.obj.mark_viewed(bundle.request)
        return bundle

    def dehydrate_num_viewers(self, bundle):
        return bundle.obj.viewers.filter(timestamp__gte=datetime.datetime.now() - datetime.timedelta(seconds=10)).count()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/ask%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('ask'), name="api_ask"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/image%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('set_image'), name="api_image"),
            url(r"^(?P<resource_name>%s)/create%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('create'), name="api_create"),
        ]



    def create(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        if not request.user.is_authenticated():
            return self.create_response(request, {
                'success': False,
                'reason': 'not_logged_in',
                }, HttpUnauthorized )
        s = AMASession()
        s.owner = request.user
        s.title = request.POST['title']
        if s.title == "":
            return self.create_response(request, {
                    'success': False,
                    'reason': 'no_title',
                }, HttpBadRequest)
        s.subtitle = request.POST['subtitle']
        if s.subtitle == "":
            return self.create_response(request, {
                    'success': False,
                    'reason': 'no_subtitle',
                }, HttpBadRequest)
        s.desc = request.POST['desc']
        if s.desc == "":
            return self.create_response(request, {
                    'success': False,
                    'reason': 'no_desc',
                }, HttpBadRequest)
        try:
            duration = float(request.POST['duration']) if request.POST['duration'] != "" else 12
            if duration < .5:
                return self.create_response(request, {
                        'success': False,
                        'reason': 'too_short',
                    }, HttpBadRequest)
            s.start_time = parser.parse('%s %s' % (request.POST['date'], request.POST['time']), ignoretz=True)
            if s.start_time.replace(tzinfo=timezone.get_current_timezone()) < timezone.now():
                s.start_time = timezone.now()
            s.end_time = s.start_time + datetime.timedelta(hours=duration)
        except:
            return self.create_response(request, {
                    'success': False,
                    'reason': 'bad_timing',
                }, HttpBadRequest)
        
        if not request.user.is_staff:
            last = request.user.sessions.order_by("-created")[:1]
            if last and last[0].created > timezone.now() - datetime.timedelta(hours=1):
                return self.create_response(request, {
                    'success': False,
                    'reason': 'too_soon',
                }, HttpBadRequest)
        try:
            file = None
            file=request.FILES['image']
            if len(file.name.split(".")) < 2 or not file.name.split(".")[-1].lower() in ("jpg, png"):
                return self.create_response(request, {
                    'success': False,
                    'reason': 'bad_image',
                }, HttpBadRequest)
            w, h = get_image_dimensions(file)
            if w < 220 or h < 220:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'small_image',
                }, HttpBadRequest)
        except KeyError:
            pass
        Request.objects.for_user(request.user).filter(session=None).update(session=s)
        if file is not None:
            file.seek(0)
            try:
                slug=base64.urlsafe_b64encode(hashlib.sha224(file.read()).digest())
                file.seek(0)
                s.image.save("%s.%s" % (slug, file.name.split(".")[-1].lower()), file)
            except:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'image_error',
                }, HttpBadRequest)
        s.save()
        return self.create_response(request, {
            'success': True,
            'slug': s.slug,
        })

    def set_image(self, request, pk, **kwargs):
        self.method_check(request, allowed=['post'])

        if not request.user.is_authenticated():
            return self.create_response(request, {
                'success': False,
                'reason': 'not_logged_in',
                }, HttpUnauthorized )

        if AMASession.objects.filter(pk=pk).count() == 0:
            return self.create_response(request, {
                'success': False,
                'reason': 'no_session',
                }, HttpBadRequest )
        s = AMASession.objects.get(pk=pk)
        if not request.user == s.owner:
            return self.create_response(request, {
                'success': False,
                'reason': 'owner',
                }, HttpUnauthorized )
        file = None
        try:
            file=request.FILES['image']
            if len(file.name.split(".")) < 2 or not file.name.split(".")[-1].lower() in ("jpg, png"):
                return self.create_response(request, {
                    'success': False,
                    'reason': 'bad_image',
                }, HttpBadRequest)
            w, h = get_image_dimensions(file)
            if w < 220 or h < 220:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'small_image',
                }, HttpBadRequest)
        except KeyError:
            pass
        if file is not None:
            file.seek(0)
            try:
                slug=base64.urlsafe_b64encode(hashlib.sha224(file.read()).digest())
                file.seek(0)
                s.image.save("%s.%s" % (slug, file.name.split(".")[-1].lower()), file)
            except:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'image_error',
                    'error': traceback.format_exc(),
                }, HttpBadRequest)
            s.save()
            return self.create_response(request, {
                'success': True,
                'slug': s.slug,
                'thumbnail': s.auto_image,
            })
        else:
            s.image = None
            s.save()
            return self.create_response(request, {
                'success': True,
                'slug': s.slug,
                'thumbnail': s.auto_image,
            })

    def ask(self, request, pk, **kwargs):
        self.method_check(request, allowed=['post'])

        if not request.user.is_authenticated():
            return self.create_response(request, {
                'success': False,
                'reason': 'not_logged_in',
                }, HttpUnauthorized )

        if AMASession.objects.filter(pk=pk).count() == 0:
            return self.create_response(request, {
                'success': False,
                'reason': 'no_session',
                }, HttpBadRequest )
        question = request.POST['question']
        desc = request.POST['desc']

        if(len(question) < 6):
            return self.create_response(request, {
                'success': False,
                'reason': 'question_short',
                }, HttpBadRequest )

        s = AMASession.objects.get(pk=pk)
        if s.after:
            return self.create_response(request, {
                'success': False,
                'reason': 'after',
                }, HttpBadRequest )
        q = AMAQuestion()
        q.asker = request.user
        q.session = s
        q.target = s.owner
        q.question = question
        q.desc = desc
        q.save()
        qr = QuestionResource()
        return self.create_response(request, {
            'success': True,
            "question": qr.full_dehydrate(qr.build_bundle(obj=q, request=request)),
            "state": s.state,
        })

class QuestionResource(ModelResource):

    answer = fields.OneToOneField('questions.api.AnswerResource', 'answer', related_name='question', null=True, full=True)
    session = fields.OneToOneField('questions.api.SessionResource', 'session', null=True)
    #comments = fields.ToManyField('questions.api.CommentResource', readonly=True, attribute='comments', null=True, use_in="detail", full=True, related_name='question')
    #html = fields.CharField(use_in = "detail")
    score = fields.IntegerField(attribute='score', default=0, readonly=True)
    asker = fields.ForeignKey('questions.api.UserResource', 'asker', full=True, readonly=True)

    class Meta:
        queryset = AMAQuestion.objects.all().order_by("-starred", "-score")
        resource_name = 'question'
        filtering = {
            'session': ALL_WITH_RELATIONS,
            'answer': ALL_WITH_RELATIONS,
            'comments': ALL_WITH_RELATIONS,
            'score': ALL
        }
        authorization = QuestionAuthorization()

    def dehydrate_html(self, bundle):
        return render_to_string("question.html", {'question': bundle.obj}, RequestContext(bundle.request))

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/vote%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('set_vote'), name="api_vote"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/answer%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('submit_answer'), name="api_answer"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/star%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('star'), name="api_star"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/comments%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_comments'), name="api_comments"),
        ]

    def get_comments(self, request, pk, **kwargs):
        return render(request, "comments.html")

    def submit_answer(self, request, pk, **kwargs):
        if not request.user.is_authenticated():
            self.method_check(request, allowed=['post'])

            return self.create_response(request, {
                'success': False,
                'reason': 'not_logged_in',
                }, HttpUnauthorized )

        try:
            q = AMAQuestion.objects.get(pk=pk)
        except AMAQuestion.DoesNotExist:
            return self.create_response(request, {
                'success': False,
                'reason': 'no_question',
                }, HttpBadRequest )

        if q.target != request.user:
            return self.create_response(request, {
                'success': False,
                'reason': 'not-target',
                }, HttpForbidden )
        if not q.session.running:
            return self.create_response(request, {
                'success': False,
                'reason': 'not_running',
                }, HttpBadRequest )
        a = request.POST.get('answer',"")
        if a == "":
            try:
                q.answer.delete()
                return self.create_response(request, {
                    'success': True,
                    'status': 'deleted'
                })
            except AMAAnswer.DoesNotExist:
                return self.create_response(request, {
                    'success': True,
                    'status': 'deleted'
                })
        else:
            try:
                answer = q.answer
                t = "edited"
            except AMAAnswer.DoesNotExist:
                answer = AMAAnswer(question=q)
                t = "created"
            answer.response = a
            answer.save()
            return self.create_response(request, {
                'success': True,
                'status': t,
            })

    def star(self, request, pk, **kwargs):
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

        vote = int(request.POST.get('star', 0))
        if not vote in (0,1):
            return self.create_response(request, {
                'success': False,
                'reason': 'bad_status',
                }, HttpBadRequest )
        question = AMAQuestion.objects.get(pk=pk)
        question.starred = bool(vote)
        question.save()
        return self.create_response(request, {
            'success': True,
        })

    def set_vote(self, request, pk, **kwargs):
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

class RequestResource(ModelResource):

    score = fields.IntegerField(attribute="score")
    vote = fields.IntegerField(attribute="vote")

    class Meta:
        queryset = Request.objects.all().order_by("-score")
        resource_name = 'request'
        filtering = {
        }

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/create%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('create'), name="api_create"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/vote%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('set_vote'), name="vote"),
        ]

    def set_vote(self, request, pk, **kwargs):
        self.method_check(request, allowed=['post'])
        if not request.user.is_authenticated():
            return self.create_response(request, {
                'success': False,
                'reason': 'not_logged_in',
                }, HttpUnauthorized )
        ama_request = get_object_or_404(Request, id=pk)
        ama_request.vote(request.user)
        return self.create_response(request, {
            'success': True,
            'tweet_url': ama_request.tweet_url
            })

    def get_object_list(self, request):
        if request.user.is_authenticated():
            return super(RequestResource, self).get_object_list(request).extra(select = {
                "vote" : """
                SELECT IFNULL(SUM(value), 0)
                FROM questions_requestvote
                WHERE questions_requestvote.request_id = questions_request.id
                AND questions_requestvote.user_id = (%d)
                """ % request.user.id
            })
        else:
            return super(RequestResource, self).get_object_list(request)

    def create(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        if not request.user.is_authenticated():
            return self.create_response(request, {
                'success': False,
                'reason': 'not_logged_in',
                }, HttpUnauthorized )
        provider = request.POST['provider']
        if not provider or not (provider in [p.id for p in providers.registry.get_list()]):
            return self.create_response(request, {
                'success': False,
                'reason': 'bad_provider',
                }, HttpBadRequest )
        username = request.POST['username']
        if not username:
            return self.create_response(request, {
                'success': False,
                'reason': 'bad_username',
                }, HttpBadRequest )
        desc = request.POST.get('desc',"")
        try:
            ama_request = Request.objects.get(provider=provider, username__iexact=username)
        except Request.DoesNotExist:
            if not request.user.is_staff and Request.objects.filter(creator=request.user, created__gte=datetime.datetime.now() - datetime.timedelta(hours=1)).count():
                return self.create_response(request, {
                    'success': False,
                    'reason': 'bad_timing',
                    }, HttpBadRequest )
            ama_request = Request(provider=provider, username=username, desc=desc, creator = request.user)
            ama_request.save()
        ama_request.vote(request.user)
        return self.create_response(request, {
            'success': True,
            'tweet_url': ama_request.tweet_url
            })

class CommentResource(ModelResource):

    user = fields.ForeignKey(UserResource, 'user', readonly=True, full=True)
    question = fields.OneToOneField('questions.api.QuestionResource', 'question')

    def hydrate(self, bundle):
        if bundle.obj.user_id is None:
            bundle.obj.user = bundle.request.user
        return bundle

    class Meta:
        queryset = Comment.objects.all().order_by("-created")
        resource_name = 'comment'
        filtering = {
            "question": ALL_WITH_RELATIONS,
            "user": ALL_WITH_RELATIONS,
            "id": ALL
        }
        authorization = CommentAuthorization()
        validation = FormValidation(form_class=CommentForm)
