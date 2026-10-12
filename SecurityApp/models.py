from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    # Usuario de Pawly: extiende el de Django con los campos del modelo de dominio (Usuario)
    LANGUAGES = [('es', 'Español'), ('en', 'English')]
    THEMES = [('light', 'Claro'), ('dark', 'Oscuro')]

    email = models.EmailField('email address', unique=True)
    is_banned = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=False)
    language = models.CharField(max_length=2, choices=LANGUAGES, default='es')
    theme = models.CharField(max_length=5, choices=THEMES, default='light')
    notify_by_email = models.BooleanField(default=True)

    class Meta:
        # Permisos que usa el rol Administrator
        permissions = [
            ('ban_user', 'Can ban users'),
            ('moderate_content', 'Can block posts and comments'),
        ]


class AuditLog(models.Model):
    # Una fila por cada acción importante del módulo de ingreso
    ACTIONS = [
        ('register', 'Register'),
        ('login', 'Login'),
        ('login_failed', 'Failed login'),
        ('logout', 'Logout'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             on_delete=models.SET_NULL, related_name='audit_logs')
    username = models.CharField(max_length=150, blank=True)
    action = models.CharField(max_length=20, choices=ACTIONS)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # La hora se muestra en la zona horaria del proyecto (Caracas)
        return f'{timezone.localtime(self.created_at):%Y-%m-%d %H:%M} {self.action} {self.username}'
