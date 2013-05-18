from django.db import models

class AMASession(models.Model):
    '''
    Question answering sessions are represented by this model.
    '''
    owner = models.ForeignKey('User', related_name='sessions', editable=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)
    
class AMAQuestion(models.Model):
    '''
    Questions asked by users are represented by this model.
    '''
    
    asker = models.ForeignKey('User', related_name='own_questions', editable=False)
    target = models.ForeignKey('User', related_name='asked_questions', editable=False)
    question = models.TextField()
    
    session = models.ForeignKey('AMASession', related_name='questions', editable=False, blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)


class AMAAnswer(models.Model):
    '''
    Answers to questions are represented by this model.
    '''
    
    question = models.OneToOneField('AMAQuestion', related_name='answer', editable=False)
    response = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)
    
class AMAVote(models.Model):
    '''
    Users' votes on questions are represented here.
    '''
    
    user = models.ForeignKey('User', related_name='votes', editable=False)
    question = models.ForeignKey('AMAQuestion', related_name='votes', editable=False)
    
    VOTE_CHOICES = (
        (1, 'Upvote'),
        (0, 'Neutral'),
        (-1, 'Downvote'),
    )
    
    value = models.IntegerField(choices=VOTE_CHOICES)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)