from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Task, Answer
from .forms import AnswerCreateForm, UserUpdateForm


def index(request):
    context = {
        'tasks': Task.objects.all(),
    }
    return render(request, template_name="index.html", context=context)


def stats(request):
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    answers = Answer.objects.all()

    teisingi = 0
    neteisingi = 0

    for answer in answers:
        if answer.is_correct():
            teisingi += 1
        else:
            neteisingi += 1

    context = {
        'num_task': Task.objects.count(),
        'num_answers_done': answers.count(),
        'num_visits': num_visits,
        'teisingi': teisingi,
        'neteisingi': neteisingi,
    }

    return render(request, "stats.html", context=context)


def task(request, pk):
    context = {
        'task': Task.objects.get(pk=pk),
    }
    return render(request, template_name="task.html", context=context)


class AnswerListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Answer
    template_name = "answers.html"
    context_object_name = "answers"

    def test_func(self):
        return self.request.user.is_staff


class AnswerDetailView(LoginRequiredMixin, DetailView):
    model = Answer
    template_name = "answer.html"
    context_object_name = "answer"


class UserAnswerListView(LoginRequiredMixin, ListView):
    model = Answer
    template_name = "user_answers.html"
    context_object_name = "answers"

    def get_queryset(self):
        return Answer.objects.filter(student=self.request.user)


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerCreateForm
    template_name = "answer_form.html"
    success_url = reverse_lazy("useranswers")

    def get_initial(self):
        return {'task': Task.objects.get(pk=self.kwargs['pk'])}

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)


class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    template_name = "answer_form.html"
    form_class = AnswerCreateForm

    def get_success_url(self):
        return reverse("answer", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.request.user.is_staff


class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    template_name = "answer_delete.html"
    context_object_name = "answer"
    success_url = reverse_lazy('answers')

    def test_func(self):
        return self.request.user.is_staff


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    template_name = "profile.html"
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user