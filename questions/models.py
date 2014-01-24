from datetime import *
from dateutil.tz import *
import random
import string

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from jsonfield import JSONField
from annoying.fields import AutoOneToOneField
from south.modelsinspector import add_introspection_rules
import django.contrib.sessions.models
from allauth.socialaccount import providers
from easy_thumbnails.fields import ThumbnailerImageField
from json import loads
from random import choice
from django import db
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.storage import staticfiles_storage

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

add_introspection_rules([], ["^annoying\.fields\.AutoOneToOneField"])

class SluggedModel(models.Model):
    slug = models.SlugField(primary_key=True, unique=True, editable=False, blank=True)

    def save(self, *args, **kwargs):
        while not self.slug:
            newslug = "".join(random.sample('1234567890abcdefghjkmnpqrstuvwxyz', 4))
            if self.__class__.objects.filter(slug=newslug).count() == 0:
                self.slug = newslug
        super(SluggedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class UserMeta(models.Model):
    user = AutoOneToOneField(User, primary_key=True, related_name="meta")
    verified = models.BooleanField(default=False)
    new = models.BooleanField(default=True)

    def answers(self):
        return AMAAnswer.objects.filter(question__target=self)

    @property
    def full_name(self):
        name = "%s %s" % (self.user.first_name, self.user.last_name)
        name = name.strip()
        return name if name else self.user.username

    @property
    def is_verified(self):
        if self.verified:
            return True
        for account in self.user.socialaccount_set.all():
            if account.provider == "twitter" and account.extra_data['verified']:
                return True
        return False

    @property 
    def auto_image(self):
        for acc in self.user.socialaccount_set.all():
            return acc.get_avatar_url()
        return staticfiles_storage.url("images/default-session.png")

    def __unicode__(self):
        return self.user.__unicode__()
    

class AMASessionManager(models.Manager):
    def get_query_set(self):
        if db.settings.DATABASES['default']['ENGINE'] == "django.db.backends.mysql":
            part = "DATE_SUB(NOW(), INTERVAL 40 second)"
        elif db.settings.DATABASES['default']['ENGINE'] == "django.db.backends.sqlite3":
            part = "datetime('now', '-40 seconds')"
        return super(AMASessionManager,self).get_query_set().extra(select={
            "num_viewers":"""
            SELECT Count(*)
            FROM questions_sessionview
            WHERE questions_sessionview.session_id = questions_amasession.slug
            AND questions_sessionview.timestamp > 
            """+part,
            "num_views":"""
            SELECT Count(*)
            FROM questions_sessionview
            WHERE questions_sessionview.session_id = questions_amasession.slug
            """
        }, select_params = [timezone.now() - timedelta(seconds=30)])

    def live(self):
        return self.all().filter(
        start_time__lt=timezone.now(),
        end_time__gt=timezone.now()).order_by('-num_viewers')

    def past(self):
        return self.all().filter(
        end_time__lt=timezone.now()).order_by('-num_views')

    def upcoming(self):
        return self.all().filter(
        start_time__gt=timezone.now()).order_by('-num_views')

class AMASession(SluggedModel):
    '''
    Question answering sessions are represented by this model.
    '''
    owner = models.ForeignKey(User, related_name='sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    title = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    desc = models.TextField(max_length=2000)
    image =  ThumbnailerImageField(upload_to="session_images", resize_source=dict(size=(220, 220), crop=True), null= True, blank = True)
    
    data = JSONField(default={}, blank=True)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    objects = AMASessionManager()
    
    def __unicode__(self):
        if self.owner.get_full_name():
            return u"%s's AMA Session" % (self.owner.get_full_name())
        else:
            return u"%s's AMA Session" % (self.owner.username)

    @property 
    def auto_image(self):
        try:
            return self.image.url
        except ValueError as e:
            for acc in self.owner.socialaccount_set.all():
                return acc.get_avatar_url()
            return staticfiles_storage.url("images/default-session.png")

    @property 
    def object(self):
        return self

    def get_marked_questions(self, request):
        return AMAQuestion.objects.vote_marked(request).filter(session=self)

    def get_absolute_url(self):
        return reverse('session', args=[self.slug])
    
    @property
    def state(self):
        if self.before:
            return "before"
        elif self.after:
            return "after"
        else:
            return "running"
    
    @property
    def absolute_url(self):
        return '/s/%i/' % self.id
    
    @property
    def unanswered(self):
        return self.questions.filter(answer=None)
    
    @property
    def answered(self):
        return self.questions.exclude(answer=None)
    
    def time_left(self):
        td = self.end_time - timezone.now()
        return ":".join(str(td).split(":")[:2])

    def time_until(self):
        td = self.start_time - timezone.now()
        return ":".join(str(td).split(":")[:2])

    @property
    def near_end(self):
        return self.end_time - timezone.now() < timedelta(minutes=30)

    @property
    def running(self):
        return self.start_time<=timezone.now()<=self.end_time

    @property
    def after(self):
        return timezone.now()>self.end_time
    
    @property
    def before(self):
        return self.start_time>timezone.now()

    def mark_viewed(self, request):
        if(request.user.is_authenticated()):
            try:
                obj = self.viewers.get(user=request.user)
            except SessionView.DoesNotExist:
                obj = SessionView(session = self, user = request.user)
            obj.save()
        else:
            if not request.session.exists(request.session.session_key):
                request.session.create() 
            try:
                obj = self.viewers.get(session_key=request.session.session_key)
            except SessionView.DoesNotExist:
                obj = SessionView(session = self, session_key=request.session.session_key)
            obj.save()

class SessionView(models.Model):
    session = models.ForeignKey(AMASession, related_name='viewers')
    user = models.ForeignKey(User, related_name='views', null=True, blank=True)
    session_key = models.CharField(max_length=256, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now = True)

class AMAQuestionManager(models.Manager):
    def get_query_set(self):
        return super(AMAQuestionManager, self).get_query_set().extra(select={
            "score":"""
            SELECT IFNULL(SUM(value), 0)
            FROM questions_amavote
            WHERE questions_amavote.question_id = questions_amaquestion.id
            """,
            "num_comments":"""
            SELECT COUNT(*)
            FROM questions_comment
            WHERE questions_comment.question_id = questions_amaquestion.id
            """
        }).order_by("-starred","-score")

    def vote_marked(self, request):
        if request.user.is_authenticated():
            return self.all().extra(select = {
                "vote" : """
                SELECT value
                FROM questions_amavote
                WHERE questions_amavote.question_id = questions_amaquestion.id
                AND questions_amavote.user_id = (%s)
                """
            }, select_params=[request.user.id])
        else:
            return self.all().extra(select = {
                "vote" : "0"
            })


class AMAQuestion(models.Model):
    '''
    Questions asked by users are represented by this model.
    '''
    
    objects = AMAQuestionManager()

    asker = models.ForeignKey(User, related_name='own_questions')
    target = models.ForeignKey(User, related_name='asked_questions')
    question = models.TextField()
    desc = models.TextField(default="")
    starred = models.BooleanField(default = False)

    data = JSONField(default={}, blank=True)
    
    session = models.ForeignKey(AMASession, related_name='questions')

    answer = models.OneToOneField('AMAAnswer', null=True, related_name="question")
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)
    
    '''@property
    def vote(self):
        try:
            return self._vote if self._vote is not None else 0
        except AttributeError:
            return 0'''
    
    def __unicode__(self):
        try:
            self.answer
        except ObjectDoesNotExist:
            return '[_]Q: %s' % self.question
        else:
            return '[X]Q: %s' % self.question

    def get_absolute_url(self):
        return reverse('question', args=[self.id])

class AMAAnswer(models.Model):
    '''
    Answers to questions are represented by this model.
    '''
    
    response = models.TextField()
    
    data = JSONField(default={}, blank=True)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)
    
    def __unicode(self):
        return 'A: %s' % response
    
class AMAVote(models.Model):

    '''
    Users' votes on questions are represented here.
    '''
    
    user = models.ForeignKey(User, related_name='votes', editable=False)
    question = models.ForeignKey(AMAQuestion, related_name='votes', editable=False)
    
    VOTE_CHOICES = (
        (1, 'Upvote'),
        (-1, 'Downvote'),
    )
    
    value = models.IntegerField(choices=VOTE_CHOICES)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        unique_together = ('user', 'question')

class RequestManager(models.Manager):
    def get_query_set(self):
        return super(RequestManager, self).get_query_set().extra(select={
            "score":"""
            SELECT IFNULL(SUM(value), 0) + questions_request.vote_weight
            FROM questions_requestvote
            WHERE questions_requestvote.request_id = questions_request.id
            """
        }).order_by("-score")

    def vote_marked(self, user):
        requests = self.all()
        if user.is_authenticated():
            return answered.extra(select = {
                "vote" : """
                SELECT IFNULL(value, 0)
                FROM questions_requestvote
                WHERE questions_requestvote.request_id = questions_request.id
                AND questions_requestvote.user_id = %s
                """
            }, select_params=[user.id])
        else:
            return answered

    def for_user(self, user):
        auths = user.socialaccount_set.all()
        if auths:
            requests = self.all()
            query = None
            for auth in auths:
                if auth.provider == "twitter":
                    part = models.Q(provider = "twitter") & models.Q(username__iexact=auth.extra_data['screen_name'])
                query = part if query is None else query | part
            requests = requests.filter(query)
            return requests
        else:
            return self.none()

tweets = [
"@%s You should do an AMA on http://ama.io.",
"@%s I'd love it if you did an AMA on http://ama.io."
]

class Request(models.Model):

    objects = RequestManager()

    username = models.CharField(max_length=255)
    provider = models.CharField(max_length=30, choices=providers.registry.as_choices())
    desc = models.TextField()
    session = models.ForeignKey(AMASession, related_name="requests", null=True, blank=True, on_delete=models.SET_NULL)
    creator = models.ForeignKey(User, related_name="requests_created", null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)
    vote_weight = models.IntegerField(default=0)

    def __unicode__(self):
        return self.username

    @property
    def tweet_url(self):
        return "https://twitter.com/intent/tweet?"+urlencode({"text": choice(tweets) % self.username.encode('utf-8')})

    @property
    def provider_object(self):
        return providers.registry.by_id(self.provider)

    def vote(self, user):
        try:
            self.votes.get(user=user)
        except RequestVote.DoesNotExist:
            RequestVote(user=user, request=self, value=1).save()
    class Meta:
        unique_together = ('username', 'provider')

class RequestVote(models.Model):

    '''
    Users' votes on requests are represented here.
    '''
    
    user = models.ForeignKey(User, related_name='request_votes', editable=False)
    request = models.ForeignKey(Request, related_name='votes', editable=False)
    
    VOTE_CHOICES = (
        (1, 'Upvote'),
    )
    
    value = models.IntegerField(choices=VOTE_CHOICES)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        unique_together = ('user', 'request')

class Comment(models.Model):

    question = models.ForeignKey(AMAQuestion, related_name = "comments")
    user = models.ForeignKey(User, related_name = "comments")

    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    comment = models.TextField()
