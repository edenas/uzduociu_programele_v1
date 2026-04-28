from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('tasks/<int:pk>/', views.task, name="task"),
    path('stats/', views.StatsView.as_view(), name="stats"),

    path('answers/', views.AnswerListView.as_view(), name="answers"),
    path('answers/<int:pk>/', views.AnswerDetailView.as_view(), name="answer"),
    path('myanswers/', views.UserAnswerListView.as_view(), name='useranswers'),
    path('tasks/<int:pk>/answercreate/', views.AnswerCreateView.as_view(), name='answer_create'),
    path('answers/<int:pk>/delete', views.AnswerDeleteView.as_view(), name='answer_delete'),

    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('tasks/manage/', views.TaskManageListView.as_view(), name='tasks_manage'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
]