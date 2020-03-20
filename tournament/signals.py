from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
import logging
import datetime

from .models import LoginTracker

error_log=logging.getLogger('error')

@receiver(user_logged_in)
def log_in(sender, user, request, **kwargs):
    try:
        #is_login_with_session_key = LoginTracker.objects.filter(session_key=request.session.session_key, user=user.id)[:1]

        #if not is_login_with_session_key:
            login_tracker = LoginTracker(user=user, session_key=request.session.session_key, login_date_time=datetime.datetime.now())
            login_tracker.save()
    except Exception as e:
        error_log.error("log_user_logged_in request: %s, error: %s" % (request, e))

@receiver(user_logged_out)
def log_out(sender, user, request, **kwargs):
    try:
        login_tracker = LoginLogoutLog.objects.filter(user=user.id, session_key=request.session.session_key)
        login_tracker.filter(logout_time__isnull=True).update(logout_time=datetime.datetime.now())
        
    except Exception as e:
        error_log.error("log_user_logged_out request: %s, error: %s" % (request, e))