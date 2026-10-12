from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.views.i18n import set_language as django_set_language

from .forms import RegisterForm
from .models import AuditLog, User
from .signals import get_ip


class LoginView(auth_views.LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    extra_context = {'title': gettext_lazy('Iniciar sesión')}

    def form_valid(self, form):
        response = super().form_valid(form)

        # Sin "Recordarme" la sesión termina al cerrar el navegador
        if not self.request.POST.get('remember'):
            self.request.session.set_expiry(0)
        return response


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        group, _created = Group.objects.get_or_create(name='Member')
        user.groups.add(group)
        AuditLog.objects.create(user=user, username=user.username, action='register', ip_address=get_ip(request))
        login(request, user)

        # Después de crear la cuenta sigue el paso 2 de 2: el perfil humano
        return redirect('profile_form')

    return render(request, 'register.html', {'form': form, 'title': _('Crear cuenta · Paso 1 de 2')})


def logout_view(request):
    # Cierra la sesión con GET o POST, porque en las pantallas es un enlace
    logout(request)
    return redirect('login')


@login_required
def profile_form(request):
    # Paso 2 de 2 del registro. Guardar el perfil humano queda para el siguiente reto
    return render(request, 'profile_form.html', {'title': _('Tu perfil · Paso 2 de 2')})


def password_reset(request):
    # Pantalla para recuperar la contraseña. El envío del correo queda para el siguiente reto
    return render(request, 'password_reset.html', {'title': _('Recuperar contraseña')})


def set_language(request):
    # Cambia el idioma de la página y, si hay sesión iniciada, lo guarda en el usuario
    response = django_set_language(request)
    language = request.POST.get('language')
    if request.user.is_authenticated and language in dict(User.LANGUAGES):
        request.user.language = language
        request.user.save(update_fields=['language'])
    return response
