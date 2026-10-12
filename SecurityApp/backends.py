from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameBackend(ModelBackend):
    # Permite entrar con el usuario o con el correo. Un usuario vetado no puede entrar

    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        if username is None or password is None:
            return None
        user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).first()
        if user is None:
            # Se calcula el hash igual, para que tarde lo mismo que con un usuario real
            User().set_password(password)
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def user_can_authenticate(self, user):
        return super().user_can_authenticate(user) and not user.is_banned
