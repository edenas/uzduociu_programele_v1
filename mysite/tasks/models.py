from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Task(models.Model):
    name = models.CharField()
    content = models.TextField()
    teacher = models.ForeignKey(to=User, on_delete=models.CASCADE)

    ANSWER_CHOICES = [
        (True, 'Taip'),
        (False, 'Ne'),
    ]

    correct_answer = models.BooleanField(choices=ANSWER_CHOICES, default=True)
    deadline = models.DateTimeField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='tasks', null=True, blank=True)

    def is_overdue(self):
        return self.deadline and timezone.now() > self.deadline

    def __str__(self):
        return self.name


class Answer(models.Model):
    task = models.ForeignKey(to="Task", on_delete=models.CASCADE)
    student = models.ForeignKey(to=User, on_delete=models.CASCADE)

    ANSWER_CHOICES = [
        (True, 'Taip'),
        (False, 'Ne'),
    ]

    answer = models.BooleanField(choices=ANSWER_CHOICES, default=True)
    date = models.DateTimeField(auto_now_add=True)

    def is_correct(self):
        return self.answer == self.task.correct_answer

    def __str__(self):
        return f"{self.task} - {self.student}"