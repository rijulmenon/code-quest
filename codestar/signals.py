from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UserActivityLog

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    UserActivityLog.objects.create(user=user, activity_type='login')

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    UserActivityLog.objects.create(user=user, activity_type='logout')

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Submission
from .tasks import process_submissions

@receiver(post_save, sender=Submission)
def submission_saved(sender, instance, created, **kwargs):
    if created:
        process_submissions.delay()