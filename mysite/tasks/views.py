from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Task, Answer
from .forms import AnswerCreateForm, UserUpdateForm


def index(request):
    context = {
        'tasks': Task.objects.all(),
    }
    return render(request, template_name="index.html", context=context)


class StatsView(LoginRequiredMixin, View):
    def get(self, request):
        num_visits = request.session.get('num_visits', 1)
        request.session['num_visits'] = num_visits + 1

        answers = Answer.objects.filter(student=request.user)

        correct_answers = 0
        incorrect_answers = 0
        late_answers = 0

        for answer in answers:
            if answer.task.deadline and answer.date > answer.task.deadline:
                late_answers += 1
            elif answer.is_correct():
                correct_answers += 1
            else:
                incorrect_answers += 1

        context = {
            'num_task': Task.objects.count(),
            'num_answers_done': answers.count(),
            'num_visits': num_visits,
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers,
            'late_answers': late_answers,
        }

        return render(request, "stats.html", context=context)


def task(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    selected_task = Task.objects.get(pk=pk)
    answered = False

    if Answer.objects.filter(task=selected_task, student=request.user).count() > 0:
        answered = True

    context = {
        'task': selected_task,
        'answered': answered,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = Task.objects.get(pk=self.kwargs['pk'])
        return context

    def get(self, request, *args, **kwargs):
        selected_task = Task.objects.get(pk=self.kwargs['pk'])

        if Answer.objects.filter(task=selected_task, student=self.request.user).count() > 0:
            return render(request, "answer_denied.html")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        selected_task = Task.objects.get(pk=self.kwargs['pk'])

        if Answer.objects.filter(task=selected_task, student=self.request.user).count() > 0:
            return render(self.request, "answer_denied.html")

        form.instance.student = self.request.user
        form.instance.task = selected_task
        return super().form_valid(form)


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