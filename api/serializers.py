from django.contrib.auth.models import User
from questions.models import AMASession, AMAQuestion
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'sessions')

class SessionSerializer(serializers.HyperlinkedModelSerializer):

    running = serializers.BooleanField(source="is_running", default=False, read_only=True, required=False)

    class Meta:
        model = AMASession
        fields = ('owner', 'start_time', 'end_time', 'questions', 'running', 'created', 'edited')
		
class QuestionSerializer(serializers.HyperlinkedModelSerializer):
	
    score = serializers.IntegerField(source='get_score', default=0, read_only=True, required=False)
    
    
    class Meta:
        model = AMAQuestion
        fields = ('asker', 'target', 'question', 'session', 'score', 'created', 'edited')