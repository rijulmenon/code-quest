from django.core.management.base import BaseCommand
from ...tasks import process_submissions

class Command(BaseCommand):
    help = 'Triggers the submission processing task'

    def handle(self, *args, **options):
        process_submissions.delay()
        self.stdout.write(self.style.SUCCESS('Submission processing task triggered'))