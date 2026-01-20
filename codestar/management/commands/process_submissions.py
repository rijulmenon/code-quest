from django.core.management.base import BaseCommand
from codestar.models import Submission

class Command(BaseCommand):
    help = 'Process all submissions'

    def handle(self, *args, **options):
        submissions = Submission.objects.select_related('user', 'question').all()
        for submission in submissions:
            # Process each submission
            pass