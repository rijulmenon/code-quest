from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('refresh-content/', views.refresh_content, name='refresh_content'),
    path('round/<int:round_id>/', views.round_questions, name='round_questions'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('question/<int:question_id>/run/', views.run_code, name='run_code'),
    path('question/<int:question_id>/submit/', views.submit_code, name='submit_code'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]