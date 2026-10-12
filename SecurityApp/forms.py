from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        # password1 y password2 vienen de UserCreationForm
        fields = ['username', 'email']
