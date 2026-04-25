from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks/<int:pk>/', views.task, name="task"),

    path('answers/', views.AnswerListView.as_view(), name="answers"),
    path('answers/<int:pk>/', views.AnswerDetailView.as_view(), name="answer"),
    path('myanswers/', views.UserAnswerListView.as_view(), name='useranswers'),
    path('tasks/<int:pk>/answercreate/', views.AnswerCreateView.as_view(), name='answer_create'),
    path('answers/<int:pk>/update', views.AnswerUpdateView.as_view(), name='answer_update'),
    path('answers/<int:pk>/delete', views.AnswerDeleteView.as_view(), name='answer_delete'),

    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
]