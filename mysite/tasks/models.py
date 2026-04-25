from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Task(models.Model):
    name = models.CharField("Užduotis")
    content = models.TextField("Klausimas")
    teacher = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Dėstytojas")

    ANSWER_CHOICES = [
        (True, 'Taip'),
        (False, 'Ne'),
    ]

    correct_answer = models.BooleanField("Teisingas atsakymas", choices=ANSWER_CHOICES, default=True)
    deadline = models.DateTimeField("Terminas", null=True, blank=True)
    date = models.DateTimeField("Data", auto_now_add=True)
    photo = models.ImageField("Nuotrauka", upload_to='tasks', null=True, blank=True)

    def is_overdue(self):
        return self.deadline and timezone.now() > self.deadline

    def __str__(self):
        return f"{self.name} - {self.content}"

    class Meta:
        verbose_name = "Uždavinys"
        verbose_name_plural = "Uždaviniai"


class Answer(models.Model):
    task = models.ForeignKey(to="Task", on_delete=models.CASCADE, verbose_name="Užduotis")
    student = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="Studentas")

    ANSWER_CHOICES = [
        (True, 'Taip'),
        (False, 'Ne'),
    ]

    answer = models.BooleanField("Atsakymas", choices=ANSWER_CHOICES, default=True)
    date = models.DateTimeField("Data", auto_now_add=True)

    def is_correct(self):
        return self.answer == self.task.correct_answer

    def __str__(self):
        return f"{self.task} - {self.student}"

    class Meta:
        verbose_name = "Atsakymas"
        verbose_name_plural = "Atsakymai"

    def answer_display(self):
        return "Taip" if self.answer else "Ne"

    def correct_display(self):
        return "Taip" if self.is_correct() else "Ne"