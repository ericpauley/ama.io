import datetime
import random
import string

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from jsonfield import JSONField
from annoying.fields import AutoOneToOneField
from south.modelsinspector import add_introspection_rules

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
    
    def __unicode__(self):
        if self.owner.get_full_name():
            return u"%s's AMA Session" % (self.owner.get_full_name())
        else:
            return u"%s's AMA Session" % (self.owner.username)

    def get_marked_questions(self, user):
        answered = self.questions.all().extra(select={
            "_score":"""
            SELECT IFNULL(SUM(value), 0)
            FROM questions_amavote
            WHERE questions_amavote.question_id = questions_amaquestion.id
            """
        }).order_by("-starred","-_score")
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
    def running(self):
        return self.start_time.replace(tzinfo=None)<datetime.datetime.now()<self.end_time.replace(tzinfo=None)
    

class AMAQuestion(models.Model):
    '''
    Questions asked by users are represented by this model.
    '''
    
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

    @property
    def score(self):
        try:
            return self._score if self._score is not None else 0
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
