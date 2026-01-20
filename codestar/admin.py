from django.contrib import admin
from .models import Round, Question, Score, UserActivityLog, Submission, TestCase, ScoringRule, Leaderboard
from django import forms
import json

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_score', 'timestamp')
    search_fields = ('user__username',)
    list_filter = ('timestamp',)

class ScoringRuleInline(admin.TabularInline):
    model = ScoringRule
    extra = 1

@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'is_active', 'score_for_correct_answer')
    list_editable = ('is_active',)
    inlines = [ScoringRuleInline]

    def score_for_correct_answer(self, obj):
        scoring_rule = ScoringRule.objects.filter(round=obj).first()
        return scoring_rule.score if scoring_rule else "Not set"
    score_for_correct_answer.short_description = "Score for Correct Answer"

class QuestionAdminForm(forms.ModelForm):
    hidden_inputs = forms.CharField(widget=forms.Textarea, required=False)
    expected_outputs = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Question
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        hidden_inputs = cleaned_data.get('hidden_inputs')
        expected_outputs = cleaned_data.get('expected_outputs')

        try:
            inputs_list = json.loads(hidden_inputs)
            outputs_list = json.loads(expected_outputs)
            if len(inputs_list) != len(outputs_list):
                raise forms.ValidationError("The number of hidden inputs and expected outputs must match.")
        except json.JSONDecodeError:
            raise forms.ValidationError("Hidden inputs and expected outputs must be valid JSON arrays.")

        return cleaned_data

from django.contrib import admin
from django import forms
from .models import Question, Submission, Round, Score, UserActivityLog

class TestCaseInline(admin.StackedInline):
    model = TestCase
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'round')
    inlines = [TestCaseInline]

# ... other admin registrations ...

from django.contrib import admin
from .models import Submission
from django.urls import reverse, path
from django.shortcuts import render, get_object_or_404
from django.utils.html import format_html

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'submitted_at', 'status', 'view_code_link')
    list_filter = ('question', 'submitted_at', 'is_correct')
    search_fields = ('user__username', 'question__title')
    readonly_fields = ('code', 'is_correct', 'execution_time')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'question')
    
    def status(self, obj):
        if obj.is_correct:
            return format_html('<span style="color: green;">Correct</span>')
        else:
            return format_html('<span style="color: red;">Incorrect</span>')
    status.short_description = 'Status'

    def view_code_link(self, obj):
        return format_html('<a href="{}">View Full Code</a>', reverse('admin:view_full_code', args=[obj.id]))
    view_code_link.short_description = 'Code'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:submission_id>/view_code/', self.admin_site.admin_view(self.view_full_code), name='view_full_code'),
        ]
        return custom_urls + urls

    def view_full_code(self, request, submission_id):
        submission = get_object_or_404(Submission, id=submission_id)
        return render(request, 'admin/view_full_code.html', {'submission': submission})

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'timestamp')

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp')
    list_filter = ('activity_type', 'timestamp')
    search_fields = ('user__username',)
    date_hierarchy = 'timestamp'


