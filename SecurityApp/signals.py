from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from .models import AuditLog


def get_ip(request):
    return request.META.get('REMOTE_ADDR') if request else None


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    AuditLog.objects.create(user=user, username=user.get_username(), action='login', ip_address=get_ip(request))


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    if user:
        AuditLog.objects.create(user=user, username=user.get_username(), action='logout', ip_address=get_ip(request))


@receiver(user_login_failed)
def log_login_failed(sender, credentials, request=None, **kwargs):
    AuditLog.objects.create(username=credentials.get('username', ''), action='login_failed', ip_address=get_ip(request))
