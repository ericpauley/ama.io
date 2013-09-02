from django import forms
from questions.models import *

class CommentForm(forms.Form):
	comment = forms.CharField(max_length = 500, min_length = 5)

	class Meta:
		model = Comment
		fields = ['question', 'comment']
