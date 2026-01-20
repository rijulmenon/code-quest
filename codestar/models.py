from django.db import models
from django.contrib.auth.models import User
import json

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-total_score']  # Order by total score descending

    def __str__(self):
        return f"{self.user.username} - {self.total_score} points"
    

class Question(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    input_format = models.TextField()
    output_format = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    round = models.ForeignKey('Round', on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.title

class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='test_cases')
    input_data = models.TextField()
    expected_output = models.TextField()  # Changed from CharField to TextField

    def __str__(self):
        return f"Test case for {self.question.title}"

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    execution_time = models.FloatField(default=0.0)  # Add this default

class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"
    
class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=10, choices=[('login', 'Login'), ('logout', 'Logout')])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.timestamp}"
    
class Round(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    is_active = models.BooleanField(default=False)
    timer_duration = models.IntegerField(default=3600)  # Timer duration in seconds

    def __str__(self):
        return self.name

class ScoringRule(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    score = models.IntegerField(help_text="Score awarded for correct answer")

    class Meta:
        ordering = ['round']

    def __str__(self):
        return f"{self.round} - {self.score} points for correct answer"