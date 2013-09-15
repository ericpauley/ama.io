from django import forms
from questions.models import *

class CommentForm(forms.Form):
	comment = forms.CharField(max_length = 500)

	class Meta:
		model = Comment
		fields = ['question', 'comment']
class SessionForm(forms.Form):
	title = forms.CharField(min_length=1, max_length=50)
	subtitle = forms.CharField(min_length=1, max_length=100)
	desc = forms.CharField(min_length=1, max_length=1000)
