from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.views.decorators.http import require_POST

from SecurityApp.models import User

from .forms import ApplicationForm, MessageForm, PetForm
from .models import Application, Chat, Message, Pet

# Opciones rápidas del formulario de postulación
HOME_OPTIONS = {
    'yard': gettext_lazy('Tengo patio'),
    'no-pets': gettext_lazy('Sin otras mascotas'),
    'kids': gettext_lazy('Tengo niños'),
    'apartment': gettext_lazy('Vivo en apartamento'),
}


def find_demo(item_id):
    # Las pantallas de ejemplo solo tienen el elemento 1
    if item_id != 1:
        raise Http404


def get_chats(user):
    chats = list(user.chats.all().order_by('-created_at'))
    for chat in chats:
        chat.other = chat.other_member(user)
    return chats


@login_required
def home(request):
    context = {'title': _('Inicio'), 'section': 'home'}
    return render(request, 'home.html', context)


@login_required
def search(request):
    context = {'title': _('Resultados para «luna»'), 'section': 'search', 'query': 'luna'}
    return render(request, 'search.html', context)


@login_required
def adoption_feed(request):
    # Mascotas en adopción de los demás usuarios
    pets = Pet.objects.filter(for_adoption=True).exclude(owner=request.user)
    context = {'title': _('Adopción'), 'section': 'adoption', 'pets': pets}
    return render(request, 'adoption_feed.html', context)


@login_required
def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, for_adoption=True)
    application = Application.objects.filter(pet=pet, applicant=request.user).first()
    context = {
        'title': f"{pet.name} · {_('Adopción')}", 'section': 'adoption', 'pet': pet, 'application': application,
    }
    return render(request, 'pet_detail.html', context)


@login_required
def application_form(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, for_adoption=True)

    # No se puede postular a su propia mascota ni dos veces a la misma
    if pet.owner == request.user or Application.objects.filter(pet=pet, applicant=request.user).exists():
        return redirect('pet_detail', pet_id=pet.id)

    form = ApplicationForm(request.POST or None)
    options = request.POST.getlist('options')
    if request.method == 'POST' and form.is_valid():
        application = form.save(commit=False)
        application.pet = pet
        application.applicant = request.user
        application.save()

        # Se abre un chat con el dueño y el mensaje de la postulación va de primero
        text = application.message
        if options:
            text += '\n\n' + ', '.join(str(HOME_OPTIONS[option]) for option in options if option in HOME_OPTIONS)
        chat = Chat.objects.create(application=application)
        chat.members.add(pet.owner, request.user)
        Message.objects.create(chat=chat, sender=request.user, text=text)
        return redirect(reverse('pet_detail', args=[pet.id]) + '?postulacion=enviada')

    context = {
        'title': _('Postularte para adoptar a %(pet)s') % {'pet': pet.name},
        'section': 'adoption', 'modal': True, 'pet': pet, 'form': form, 'options': options,
    }
    return render(request, 'application_form.html', context)


@login_required
def chat_list(request):
    context = {'title': _('Mensajes'), 'section': 'messages', 'chats': get_chats(request.user)}
    return render(request, 'chat_list.html', context)


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, members=request.user)
    form = MessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        message = form.save(commit=False)
        message.chat = chat
        message.sender = request.user
        message.save()
        return redirect('chat_detail', chat_id=chat.id)

    other = chat.other_member(request.user)
    context = {
        'title': _('Conversación con %(name)s') % {'name': other.display_name()}, 'section': 'messages',
        'chat': chat, 'other': other, 'chats': get_chats(request.user), 'form': form,
    }
    return render(request, 'chat_detail.html', context)


@login_required
@require_POST
def application_cancel(request, chat_id):
    # Solo quien se postuló puede cancelar
    chat = get_object_or_404(Chat, id=chat_id, application__applicant=request.user)
    chat.application.status = 'cancelled'
    chat.application.save()
    return redirect('chat_detail', chat_id=chat.id)


@login_required
def notifications(request):
    context = {'title': _('Notificaciones'), 'section': 'notifications'}
    return render(request, 'notifications.html', context)


@login_required
def my_profile(request):
    context = {
        'title': _('Mi perfil'), 'section': 'profile', 'pets': request.user.pets.all(),
        'applications': request.user.applications.all(),
    }
    return render(request, 'my_profile.html', context)


@login_required
def account_settings(request):
    context = {'title': _('Ajustes'), 'section': 'profile'}
    return render(request, 'account_settings.html', context)


@login_required
def pet_profile(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    context = {'title': f"{pet.name} · {_('Mis mascotas')}", 'section': 'profile', 'pet': pet}
    return render(request, 'pet_profile.html', context)


@login_required
def pet_create(request):
    return pet_form(request, Pet(owner=request.user), _('Nueva mascota'))


@login_required
def pet_edit(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    return pet_form(request, pet, _('Editar a %(name)s') % {'name': pet.name})


def pet_form(request, pet, title):
    # Crear y editar usan el mismo formulario
    form = PetForm(request.POST or None, request.FILES or None, instance=pet)
    if request.method == 'POST':
        temperament = request.POST.getlist('temperament')
        if form.is_valid():
            pet = form.save(commit=False)
            pet.temperament = ','.join(temperament)
            pet.save()
            return redirect('pet_profile', pet_id=pet.id)
    else:
        temperament = pet.temperament.split(',')

    context = {'title': title, 'section': 'profile', 'pet': pet, 'form': form, 'temperament': temperament}
    return render(request, 'pet_edit.html', context)


@login_required
@require_POST
def pet_delete(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    pet.delete()
    return redirect('my_profile')


@login_required
def user_profile(request, user_id):
    find_demo(user_id)
    context = {'title': 'Laura Barreto', 'section': 'search'}
    return render(request, 'user_profile.html', context)


@login_required
def post_create(request):
    context = {'title': _('Nueva publicación'), 'section': 'home', 'modal': True}
    return render(request, 'post_create.html', context)


@login_required
def post_detail(request, post_id):
    find_demo(post_id)
    context = {'title': _('Publicación de Andrea Salas'), 'section': 'home'}
    return render(request, 'post_detail.html', context)


@login_required
def report(request, post_id):
    find_demo(post_id)
    context = {'title': _('Reportar publicación'), 'section': 'home', 'modal': True}
    return render(request, 'report.html', context)


# Solo entra el rol administrador
@login_required
@permission_required('SecurityApp.moderate_content', raise_exception=True)
def admin_panel(request):
    context = {
        'title': _('Panel de administración'),
        'users': User.objects.annotate(pets_count=Count('pets')).order_by('-date_joined')[:10],
        'active_users': User.objects.filter(is_active=True).count(),
        'pets_count': Pet.objects.count(),
        'adoption_count': Pet.objects.filter(for_adoption=True).count(),
        'applications_count': Application.objects.count(),
    }
    return render(request, 'admin_panel.html', context)


@login_required
@permission_required('SecurityApp.ban_user', raise_exception=True)
@require_POST
def user_ban(request, user_id):
    account = get_object_or_404(User, id=user_id)

    # Vetar o quitar el veto, el administrador no se puede vetar a sí mismo
    if account != request.user:
        account.is_active = not account.is_active
        account.save()
    return redirect('admin_panel')
