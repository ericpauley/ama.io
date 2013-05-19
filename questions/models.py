from django.db import models
from django.contrib.auth.models import User

class AMASession(models.Model):
    '''
    Question answering sessions are represented by this model.
    '''
    owner = models.ForeignKey(User, related_name='sessions', editable=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)
    
    def __unicode__(self):
        if user.first_name is not None and user.last_name is not None:
            return u"%s %s's AMA Session" % (user.first_name, user.last_name)
        else:
            return u"%s's AMA Session" % user.username
        
    def get_absolute_url(self):
        return '/s/%i/' % self.id
    
class AMAQuestion(models.Model):
    '''
    Questions asked by users are represented by this model.
    '''
    
    asker = models.ForeignKey(User, related_name='own_questions', editable=False)
    target = models.ForeignKey(User, related_name='asked_questions', editable=False)
    question = models.TextField()
    
    session = models.ForeignKey(AMASession, related_name='questions', editable=False, blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)
    
    def __unicode__(self):
        if answer:
            return '[X]Q: %s' % question
        else:
            return '[_]Q: %s' % question

class AMAAnswer(models.Model):
    '''
    Answers to questions are represented by this model.
    '''
    
    question = models.OneToOneField(AMAQuestion, related_name='answer', editable=False)
    response = models.TextField()
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True, editable=False)
    
    def __unicode(self):
        return 'A: %s' % response
    
# class AMAVote(models.Model):
#     '''
#     Users' votes on questions are represented here.
#     '''
#     
#     user = models.ForeignKey(User, related_name='votes', editable=False)
#     question = models.ForeignKey(AMAQuestion, related_name='votes', editable=False)
#     
#     VOTE_CHOICES = (
#         (1, 'Upvote'),
#         (0, 'Neutral'),
#         (-1, 'Downvote'),
#     )
#     
#     value = models.IntegerField(choices=VOTE_CHOICES)
#     
#     created = models.DateTimeField(auto_now_add=True, editable=False)
#     edited = models.DateTimeField(auto_now=True, editable=False)
#     
#     class Meta:
#         unique_together = ('user', 'question')
