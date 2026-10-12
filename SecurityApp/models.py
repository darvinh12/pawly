from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)

    class Meta:
        # Permisos del rol administrador
        permissions = [
            ('ban_user', 'Can ban users'),
            ('moderate_content', 'Can block posts and comments'),
        ]

    # Nombre del perfil o el usuario si aún no tiene perfil
    def display_name(self):
        profile = getattr(self, 'profile', None)
        if profile and profile.full_name:
            return profile.full_name
        return self.username

    def avatar_url(self):
        profile = getattr(self, 'profile', None)
        if profile and profile.photo:
            return profile.photo.url
        return settings.MEDIA_URL + 'avatars/avatar-h.svg'


class AuditLog(models.Model):
    # Registro de las acciones del módulo de ingreso
    ACTIONS = [
        ('register', 'Register'),
        ('login', 'Login'),
        ('login_failed', 'Failed login'),
        ('logout', 'Logout'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    username = models.CharField(max_length=150, blank=True)
    action = models.CharField(max_length=20, choices=ACTIONS)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} {self.action}'
