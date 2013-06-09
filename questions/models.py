from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from jsonfield import JSONField

import datetime

import string
import random

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

class AMASession(SluggedModel):
    '''
    Question answering sessions are represented by this model.
    '''
    owner = models.ForeignKey(User, related_name='sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    data = JSONField(default={}, blank=True)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)
    
    def __unicode__(self):
        if self.owner.get_full_name():
            return u"%s's AMA Session" % (self.owner.get_full_name())
        else:
            return u"%s's AMA Session" % (self.owner.username)
        
    def get_absolute_url(self):
        return '/s/%i/' % self.id
        
    def get_unanswered(self):
        return self.questions.filter(answer=None).annotate(score=models.Sum('votes__value'))
        
    def get_answered(self):
        return self.questions.exclude(answer=None).annotate(score=models.Sum('votes__value'))
        
    def is_running(self):
        return self.start_time.replace(tzinfo=None)<datetime.datetime.now()<self.end_time.replace(tzinfo=None)
    
class AMAQuestion(models.Model):
    '''
    Questions asked by users are represented by this model.
    '''
    
    asker = models.ForeignKey(User, related_name='own_questions')
    target = models.ForeignKey(User, related_name='asked_questions')
    question = models.TextField()
    
    data = JSONField(default={}, blank=True)
    
    session = models.ForeignKey(AMASession, related_name='questions')
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)
    
    def get_score(self):
        try:
            return self.score if score is not None else 0
        except:
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
        (0, 'Neutral'),
        (-1, 'Downvote'),
    )
    
    value = models.IntegerField(choices=VOTE_CHOICES)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)
    
    class Meta:
        unique_together = ('user', 'question')
