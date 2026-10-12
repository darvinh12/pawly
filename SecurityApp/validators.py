from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class NumberValidator:
    # La contraseña debe tener al menos un número, como dice la pantalla de registro

    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('La contraseña debe tener al menos un número.'), code='password_no_number')

    def get_help_text(self):
        return _('Tu contraseña debe tener al menos un número.')
