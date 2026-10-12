from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Application, Message, Pet, Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'national_id', 'photo', 'birth_date', 'gender', 'city', 'about']
        error_messages = {
            'full_name': {'required': _('Escribe tu nombre completo')},
            'national_id': {'required': _('Escribe tu cédula')},
        }


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'sex', 'birth_date', 'about', 'photo', 'for_adoption', 'family', 'location']
        error_messages = {
            'name': {'required': _('Escribe el nombre de tu mascota')},
        }

    def clean(self):
        cleaned_data = super().clean()
        # Para ponerla en adopción hay que decir qué familia busca
        if cleaned_data.get('for_adoption') and not cleaned_data.get('family', '').strip():
            self.add_error('family', _('Cuéntanos qué familia buscas para tu mascota'))
        return cleaned_data


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message']
        error_messages = {
            'message': {'required': _('Escribe un mensaje para el dueño')},
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
