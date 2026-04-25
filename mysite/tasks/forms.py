from django import forms
from django.contrib.auth.models import User
from .models import Answer


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['task', 'answer']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']