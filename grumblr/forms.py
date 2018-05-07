from django import forms
from django.contrib.auth.forms import UserCreationForm
from grumblr.models import *

class LoginForm(forms.Form):
	username = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'username'}))
	password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder':'password'}))



class RegisterForm(UserCreationForm):
	email = forms.EmailField(label='Email')
	firstname = forms.CharField(label='Firstname')
	lastname = forms.CharField(label='Lastname')


class PostForm(forms.Form):
	content = forms.CharField(label='')

class Comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile 
		exclude = ('owner', 'follow',)
		widgets = {'photo':forms.FileInput()}
