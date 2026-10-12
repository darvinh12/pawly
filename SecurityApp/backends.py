from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import User


class EmailOrUsernameBackend(ModelBackend):
    # Permite entrar con el usuario o con el correo

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).first()
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
