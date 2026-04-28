from django import forms
from django.contrib.auth.models import User
from .models import Answer, Task


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']


class TaskCreateForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        label="Galioja iki:",
        required=False,
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            },
            format='%Y-%m-%dT%H:%M'
        )
    )

    class Meta:
        model = Task
        fields = ['name', 'content', 'correct_answer', 'deadline', 'photo']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']