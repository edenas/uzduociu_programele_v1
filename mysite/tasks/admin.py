from django.contrib import admin
from .models import Task, Answer


class TaskAdmin(admin.ModelAdmin):
    list_display = ['uzduotis', 'destytojas', 'teisingas_atsakymas', 'terminas', 'statusas']

    def uzduotis(self, task):
        return task.name

    def destytojas(self, task):
        return task.teacher

    def teisingas_atsakymas(self, task):
        if task.correct_answer:
            return "Taip"
        else:
            return "Ne"

    def terminas(self, task):
        return task.deadline

    def statusas(self, task):
        if task.is_overdue():
            return "Pradelsta"
        else:
            return "Laiku"

    uzduotis.short_description = "Užduotis"
    destytojas.short_description = "Dėstytojas"
    teisingas_atsakymas.short_description = "Teisingas atsakymas"
    terminas.short_description = "Terminas"
    statusas.short_description = "Statusas"


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['uzduotis', 'studentas', 'atsakymas', 'ar_gerai_atsake', 'data']

    def uzduotis(self, answer):
        return answer.task

    def studentas(self, answer):
        return answer.student

    def atsakymas(self, answer):
        if answer.answer:
            return "Taip"
        else:
            return "Ne"

    def ar_gerai_atsake(self, answer):
        if answer.is_correct():
            return "Taip"
        else:
            return "Ne"

    def data(self, answer):
        return answer.date

    uzduotis.short_description = "Užduotis"
    studentas.short_description = "Studentas"
    atsakymas.short_description = "Atsakymas"
    ar_gerai_atsake.short_description = "Ar gerai atsakė"
    data.short_description = "Data"


admin.site.register(Task, TaskAdmin)
admin.site.register(Answer, AnswerAdmin)