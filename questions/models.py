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
from allaccess.models import Provider
import django.contrib.sessions.models

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

    @property
    def full_name(self):
        name = "%s %s" % (self.user.first_name, self.user.last_name)
        name = name.strip()
        return name if name else self.user.username

class AMASessionManager(models.Manager):
    def get_query_set(self):
        return super(AMASessionManager,self).get_query_set().extra(select={
            "num_viewers":"""
            SELECT Count(*)
            FROM questions_sessionview
            WHERE questions_sessionview.session_id = questions_amasession.slug
            AND questions_sessionview.timestamp > DATETIME('%s')
            """ % (datetime.utcnow() - timedelta(minutes=.1)).isoformat()
        })

class AMASession(SluggedModel):
    '''
    Question answering sessions are represented by this model.
    '''
    owner = models.ForeignKey(User, related_name='sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    title = models.CharField(max_length=30)
    subtitle = models.CharField(max_length=50)
    desc = models.TextField()
    image = models.ImageField(upload_to="session_images")
    
    data = JSONField(default={}, blank=True)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    objects = AMASessionManager()
    
    def __unicode__(self):
        if self.owner.get_full_name():
            return u"%s's AMA Session" % (self.owner.get_full_name())
        else:
            return u"%s's AMA Session" % (self.owner.username)

    def get_marked_questions(self, user):
        answered = self.questions.all()
        if user.is_authenticated():
            return answered.extra(select = {
                "_vote" : """
                SELECT value
                FROM questions_amavote
                WHERE questions_amavote.question_id = questions_amaquestion.id
                AND questions_amavote.user_id = (%d)
                """ % user.id
            })
        else:
            return answered
    
    @property
    def absolute_url(self):
        return '/s/%i/' % self.id
    
    @property
    def unanswered(self):
        return self.questions.filter(answer=None).annotate(score=models.Sum('votes__value')).order_by("-starred","-_score")
    
    @property
    def answered(self):
        return self.questions.exclude(answer=None).annotate(score=models.Sum('votes__value')).order_by("-starred","-_score")
    
    @property
    def time_left(self):
        return timedelta(seconds=int((self.end_time - datetime.now(tzlocal())).total_seconds()))

    @property
    def time_until(self):
        return timedelta(seconds=int((self.start_time - datetime.now(tzlocal())).total_seconds()))

    @property
    def near_end(self):
        return self.end_time - datetime.now(tzlocal()) < timedelta(minutes=30)

    @property
    def running(self):
        return self.start_time<=datetime.now(tzlocal())<=self.end_time

    @property
    def after(self):
        return datetime.now(tzlocal())>self.end_time
    
    @property
    def before(self):
        return self.start_time>datetime.now(tzlocal())

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
            session = django.contrib.sessions.models.Session.objects.get(session_key=request.session.session_key)
            try:
                obj = self.viewers.get(user_session=session)
            except SessionView.DoesNotExist:
                obj = SessionView(session = self, user_session = session)
            obj.save()


class SessionView(models.Model):
    session = models.ForeignKey(AMASession, related_name='viewers')
    user = models.ForeignKey(User, related_name='views', null=True)
    user_session = models.ForeignKey(django.contrib.sessions.models.Session, related_name='views', null=True)
    timestamp = models.DateTimeField(auto_now = True)

class AMAQuestionManager(models.Manager):
    def get_query_set(self):
        return super(AMAQuestionManager, self).get_query_set().extra(select={
            "score":"""
            SELECT IFNULL(SUM(value), 0)
            FROM questions_amavote
            WHERE questions_amavote.question_id = questions_amaquestion.id
            """
        }).order_by("-starred","-score")

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
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)
    
    @property
    def vote(self):
        try:
            return self._vote if self._vote is not None else 0
        except AttributeError:
            return 0
    
    def __unicode__(self):
        try:
            self.answer
        except ObjectDoesNotExist:
            return '[_]Q: %s' % self.question
        else:
            return '[X]Q: %s' % self.question

class AMAAnswer(models.Model):
    '''
    Answers to questions are represented by this model.
    '''
    
    question = models.OneToOneField(AMAQuestion, related_name='answer')
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
            SELECT IFNULL(SUM(value), 0)
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
                AND questions_requestvote.user_id = (%d)
                """ % user.id
            })
        else:
            return answered

class Request(models.Model):

    objects = RequestManager()

    person = models.CharField(max_length=255)
    provider = models.ForeignKey(Provider, related_name="requests")
    desc = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = ('person', 'provider')

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
