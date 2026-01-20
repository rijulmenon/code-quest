import sys
from io import StringIO
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Submission, Round, Score,ScoringRule, Leaderboard
from datetime import timedelta
from django.contrib.auth import logout
from itertools import zip_longest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils import evaluate_code
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_page

@cache_page(60)
@login_required
def leaderboard(request):
    leaderboard_entries = Leaderboard.objects.all()  # Fetch all leaderboard entries
    return render(request, 'codestar/leaderboard.html', {'leaderboard_entries': leaderboard_entries})

@login_required
@require_GET
def refresh_content(request):
    active_rounds = Round.objects.filter(is_active=True).order_by('number')
    user_score, _ = Score.objects.get_or_create(user=request.user)
    
    rounds_data = [{'id': round.id, 'name': round.name} for round in active_rounds]
    
    return JsonResponse({
        'rounds': rounds_data,
        'user_score': user_score.score
    })

import json
import subprocess
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Question, Submission
import traceback
from .code_execution import execute_user_code

import time
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def submit_code(request, question_id):
    try:
        data = json.loads(request.body)
        code = data['code']
        question = get_object_or_404(Question, id=question_id)
        test_cases = question.test_cases.all()
        results = []

        for test_case in test_cases:
            try:
                output = execute_user_code(code, test_case.input_data)
                expected_output = '\n'.join(line.strip() for line in test_case.expected_output.strip().split('\n'))
                actual_output = '\n'.join(line.strip() for line in output.strip().split('\n'))
                correct = actual_output == expected_output
                results.append({
                    'input': test_case.input_data,
                    'expected': expected_output,
                    'actual': actual_output,
                    'correct': correct,
                })
            except Exception as e:
                print(f"Error executing code: {str(e)}")
                results.append({
                    'input': test_case.input_data,
                    'error': str(e),
                    'correct': False,
                })

        all_correct = all(result['correct'] for result in results)
        score = 0
        if all_correct:
            # Get the round for this question
            round = question.round
            
            # Find the appropriate scoring rule
            scoring_rule = ScoringRule.objects.filter(round=round).first()

            if scoring_rule:
                score = scoring_rule.score
            else:
                score = 0  # Default score if no rule matches

            # Update user's score
            user_score, created = Score.objects.get_or_create(user=request.user)
            user_score.score += score
            user_score.save()

            leaderboard_entry, created = Leaderboard.objects.get_or_create(user=request.user)
            leaderboard_entry.total_score += score
            leaderboard_entry.save()

        # Create a new submission
        Submission.objects.create(
            user=request.user,
            question=question,
            code=code,
            is_correct=all_correct,
        )

        return JsonResponse({
            'success': True,
            'message': 'Code submitted successfully',
            'all_correct': all_correct,
            'score': score,
            'results': results
        })

    except Exception as e:
        print(f"Error in submit_code: {str(e)}")
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required
def home(request):
    rounds = Round.objects.filter(is_active=True).order_by('number')
    user_score, created = Score.objects.get_or_create(user=request.user)
    
    context = {
        'rounds': rounds,
        'user_score': user_score.score,
    }
    return render(request, 'codestar/home.html', context)

@login_required
def round_questions(request, round_id):
    round = get_object_or_404(Round, id=round_id)
    questions = round.questions.all()
    
    # Get the IDs of questions solved by the current user
    solved_questions = Submission.objects.filter(
        user=request.user,
        question__round=round,
        is_correct=True
    ).values_list('question_id', flat=True)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        questions_data = [
            {
                'id': q.id,
                'title': q.title,
                'is_solved': q.id in solved_questions
            } for q in questions
        ]
        return JsonResponse({
            'round': round.name,
            'questions': questions_data
        })

    context = {
        'round': round,
        'questions': questions,
        'solved_questions': solved_questions,
    }
    return render(request, 'codestar/round_questions.html', context)

from django.shortcuts import render
from .tasks import process_submissions

def trigger_submission_processing(request):
    process_submissions.delay()
    return render(request, 'processing_started.html')

from .models import Submission

def submission_list_view(request):
    submissions = Submission.objects.select_related('user', 'question').all()
    return render(request, 'submission_list.html', {'submissions': submissions})
@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    submission = Submission.objects.filter(user=request.user, question=question).first()
    return JsonResponse({
        'title': question.title,
        'description': question.description,
        'input_format': question.input_format,
        'output_format': question.output_format,
        'sample_input': question.sample_input,
        'sample_output': question.sample_output,
        'submission_code': submission.code if submission else '',
        'input_data': '',  # You can add this if needed
        'output': ''  # You can add this if needed
    })

import io
import sys
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def run_code(request, question_id):
    data = json.loads(request.body)
    code = data['code']
    input_data = data['input']

    # Redirect stdout to capture print output
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()

    try:
        # Create a dictionary to simulate the global namespace
        namespace = {}
        
        # Simulate multiple input() calls by splitting the input string
        input_lines = input_data.split('\n')
        input_iterator = iter(input_lines)
        
        # Replace the built-in input function
        def custom_input(prompt=''):
            try:
                return next(input_iterator)
            except StopIteration:
                raise EOFError("No more input available")

        namespace['input'] = custom_input

        # Execute the code
        exec(code, namespace)

        # Get the captured output
        output = mystdout.getvalue()

        return JsonResponse({'output': output})
    except Exception as e:
        return JsonResponse({'output': 'Error'})
    finally:
        sys.stdout = old_stdout

from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect

# Add this new view
def logout_view(request):
    auth_logout(request)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    else:
        messages.info(request, 'You have been logged out.')
        return redirect('/accounts/login/')  # Make sure 'login' is the correct name for your login URL