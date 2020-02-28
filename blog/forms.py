from django import forms
from .models import Comment



class PostShareForm(forms.Form):

	name 	= forms.CharField()
	email	= forms.EmailField()
	to 		= forms.EmailField()
	comment = forms.CharField()


class CommentForm(forms.ModelForm):

	class Meta:

		model 	= Comment
		fields	= ('name','email','content')


class SearchForm(forms.Form):
	query = forms.CharField()		