from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from .models import Post


# Datos de ejemplo para las pantallas. Los modelos de mascota, publicación y chat se construyen en el
# siguiente reto, y entonces estas listas y las pantallas de ejemplo usan consultas a la base de datos.
MY_PETS = [
    {
        'id': 1, 'name': 'Mía', 'photo': 'pets/d5.jpg', 'alt': 'Mía, pastora alemana, echada en el pasto',
        'location': 'Ocumare del Tuy, Miranda', 'species': 'Perro · Pastor alemán', 'age': '5 años',
        'sex': 'Hembra', 'temperament': 'Juguetona, sociable',
        'about': 'Pastor alemán de 5 años muy cariñosa y acostumbrada a niños 🐕 le encanta el parque y dormir en el sofá',
        'wants': 'Familia con tiempo para pasear y sin niños muy pequeños, preferiblemente en Caracas o los Valles del Tuy',
    },
]

ADOPTION_PETS = [
    {'id': 1, 'name': 'Toby', 'location': 'Chacao, Caracas', 'photo': 'pets/d1.jpg',
     'alt': 'Toby, perro mestizo de pelo gris, durmiendo en una cama', 'distance': 2, 'breed': 'Mestizo',
     'age': '2 años', 'sex': 'Macho', 'place': 'Chacao', 'owner': 'Luis García', 'species': 'Perro · Mestizo',
     'temperament': 'Tranquilo',
     'about': 'Tranquilo, juguetón y muy apegado. Se lleva bien con niños y otros perros, tiene sus vacunas al día y está esterilizado. Lo rescatamos en La Candelaria hace un año y ya está listo para su hogar definitivo.',
     'wants': 'Tenga patio o salga a caminar a diario y esté en Caracas o los Valles del Tuy para poder hacer la visita previa.',
     'published': '10 sep 2026', 'published_iso': '2026-09-10', 'owner_adoptions': '2 adopciones logradas'},
    {'id': 2, 'name': 'Nala', 'location': 'La Candelaria, Caracas', 'photo': 'pets/c1.jpg',
     'alt': 'Nala, gata atigrada gris, mirando a la cámara', 'distance': 3, 'breed': 'Gata', 'age': '1 año',
     'sex': 'Hembra', 'place': 'La Candelaria', 'owner': 'Lunita Rescates', 'species': 'Gato · Atigrada',
     'temperament': 'Cariñosa',
     'about': 'Gata atigrada de 1 año muy cariñosa. Está vacunada y esterilizada, se lleva bien con otros gatos y le encanta dormir al sol.',
     'wants': 'Un hogar tranquilo, con las ventanas protegidas, en Caracas o los Valles del Tuy.',
     'published': '12 sep 2026', 'published_iso': '2026-09-12', 'owner_adoptions': '12 adopciones logradas'},
    {'id': 3, 'name': 'Rocky', 'location': 'Los Palos Grandes, Caracas', 'photo': 'pets/d3.jpg',
     'alt': 'Rocky, perro con collar rojo, sonriendo sobre el pasto', 'distance': 4, 'breed': 'Beagle',
     'age': '4 años', 'sex': 'Macho', 'place': 'Los Palos Grandes', 'owner': 'Daniela Bracho',
     'species': 'Perro · Beagle', 'temperament': 'Enérgico',
     'about': 'Beagle de 4 años muy alegre y curioso. Tiene sus vacunas al día y necesita paseos largos todos los días.',
     'wants': 'Familia activa, con patio o cerca de un parque, en Caracas.',
     'published': '8 sep 2026', 'published_iso': '2026-09-08', 'owner_adoptions': '1 adopción lograda'},
    {'id': 4, 'name': 'Kira', 'location': 'Baruta, Miranda', 'photo': 'pets/d4.jpg',
     'alt': 'Kira, cachorra de pelo blanco, echada en la playa', 'distance': 6, 'breed': 'Mestiza',
     'age': '8 meses', 'sex': 'Hembra', 'place': 'Baruta', 'owner': 'Luna Martínez', 'species': 'Perro · Mestiza',
     'temperament': 'Juguetona',
     'about': 'Cachorra de 8 meses, juguetona y muy dulce. Ya tiene sus primeras vacunas y está aprendiendo a pasear con correa.',
     'wants': 'Una familia con paciencia para enseñarle y con tiempo para jugar.',
     'published': '14 sep 2026', 'published_iso': '2026-09-14', 'owner_adoptions': '3 adopciones logradas'},
    {'id': 5, 'name': 'Bruno', 'location': 'El Hatillo, Miranda', 'photo': 'pets/d7.jpg',
     'alt': 'Bruno, perro tricolor, echado en su cama', 'distance': 7, 'breed': 'Labrador', 'age': '3 años',
     'sex': 'Macho', 'place': 'El Hatillo', 'owner': 'Pedro Ramírez', 'species': 'Perro · Labrador',
     'temperament': 'Noble',
     'about': 'Labrador de 3 años tranquilo y muy noble, se lleva bien con niños. Está esterilizado y tiene todas sus vacunas.',
     'wants': 'Una familia con espacio para que corra, en Caracas o Miranda.',
     'published': '5 sep 2026', 'published_iso': '2026-09-05', 'owner_adoptions': '4 adopciones logradas'},
    {'id': 6, 'name': 'Coco', 'location': 'Petare, Miranda', 'photo': 'pets/d8.jpg',
     'alt': 'Coco, perro de pelo claro, sentado en el piso', 'distance': 9, 'breed': 'Mestizo', 'age': '5 años',
     'sex': 'Macho', 'place': 'Petare', 'owner': 'José Gutiérrez', 'species': 'Perro · Mestizo',
     'temperament': 'Tranquilo',
     'about': 'Mestizo de 5 años, tranquilo y obediente. Fue rescatado hace dos años y está listo para un hogar definitivo.',
     'wants': 'Una familia paciente, de preferencia sin otros perros.',
     'published': '2 sep 2026', 'published_iso': '2026-09-02', 'owner_adoptions': '1 adopción lograda'},
    {'id': 7, 'name': 'Simón', 'location': 'Los Teques, Miranda', 'photo': 'pets/c2.jpg',
     'alt': 'Simón, gatito atigrado, asomado en un túnel de tela', 'distance': 12, 'breed': 'Gato',
     'age': '8 meses', 'sex': 'Macho', 'place': 'Los Teques', 'owner': 'Luna Delgado', 'species': 'Gato · Atigrado',
     'temperament': 'Curioso',
     'about': 'Gatito atigrado de 8 meses, curioso y juguetón. Ya está desparasitado y usa su caja de arena.',
     'wants': 'Un hogar con rascadores y ventanas seguras, en los Altos Mirandinos.',
     'published': '15 sep 2026', 'published_iso': '2026-09-15', 'owner_adoptions': '2 adopciones logradas'},
    {'id': 8, 'name': 'Max', 'location': 'Guarenas, Miranda', 'photo': 'pets/d9.jpg',
     'alt': 'Max, perro de pelo marrón, echado en el pasto', 'distance': 18, 'breed': 'Pastor alemán',
     'age': '6 años', 'sex': 'Macho', 'place': 'Guarenas', 'owner': 'Valentina Ochoa',
     'species': 'Perro · Pastor alemán', 'temperament': 'Protector',
     'about': 'Pastor alemán de 6 años, leal y protector. Tiene sus vacunas al día y le gusta caminar por las mañanas.',
     'wants': 'Una familia con experiencia con perros grandes y con patio, en Miranda.',
     'published': '1 sep 2026', 'published_iso': '2026-09-01', 'owner_adoptions': '5 adopciones logradas'},
]


def find_pet(pets, pet_id):
    for pet in pets:
        if pet['id'] == pet_id:
            return pet
    raise Http404


def find_demo(item_id):
    # Las pantallas de ejemplo solo tienen un elemento, el número 1
    if item_id != 1:
        raise Http404


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
    context = {'title': _('Adopción'), 'section': 'adoption', 'pets': ADOPTION_PETS}
    return render(request, 'adoption_feed.html', context)


@login_required
def pet_detail(request, pet_id):
    pet = find_pet(ADOPTION_PETS, pet_id)
    context = {
        'title': f"{pet['name']} · {_('Adopción')}", 'section': 'adoption', 'pet': pet,
        'owner_first_name': pet['owner'].split()[0],
    }
    return render(request, 'pet_detail.html', context)


@login_required
def application_form(request, pet_id):
    pet = find_pet(ADOPTION_PETS, pet_id)
    owner_first_name = pet['owner'].split()[0]
    message = _('Hola %(owner)s, vivo en Ocumare del Tuy tengo patio y salgo a caminar todas las mañanas, '
                'me encantaría conocer a %(pet)s este fin de semana') % {'owner': owner_first_name, 'pet': pet['name']}
    options = ['yard', 'no-pets']
    error = ''

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        options = request.POST.getlist('options')
        if message:
            # Pendiente del siguiente reto: guardar la postulación y abrir el chat con el dueño
            return redirect(reverse('pet_detail', args=[pet_id]) + '?postulacion=enviada')
        error = _('Escribe un mensaje para el dueño')

    context = {
        'title': _('Postularte para adoptar a %(pet)s') % {'pet': pet['name']},
        'section': 'adoption', 'modal': True, 'pet': pet, 'owner_first_name': owner_first_name,
        'message': message, 'options': options, 'error': error,
    }
    return render(request, 'application_form.html', context)


@login_required
def chat_list(request):
    context = {'title': _('Mensajes'), 'section': 'messages'}
    return render(request, 'chat_list.html', context)


@login_required
def chat_detail(request, chat_id):
    find_demo(chat_id)
    context = {'title': _('Conversación con Luis García'), 'section': 'messages'}
    return render(request, 'chat_detail.html', context)


@login_required
def notifications(request):
    context = {'title': _('Notificaciones'), 'section': 'notifications'}
    return render(request, 'notifications.html', context)


@login_required
def my_profile(request):
    context = {'title': _('Mi perfil'), 'section': 'profile'}
    return render(request, 'my_profile.html', context)


@login_required
def account_settings(request):
    context = {'title': _('Ajustes'), 'section': 'profile'}
    return render(request, 'account_settings.html', context)


@login_required
def pet_profile(request, pet_id):
    pet = find_pet(MY_PETS, pet_id)
    context = {'title': f"{pet['name']} · {_('Mis mascotas')}", 'section': 'profile', 'pet': pet}
    return render(request, 'pet_profile.html', context)


@login_required
def pet_edit(request, pet_id):
    pet = find_pet(MY_PETS, pet_id)
    context = {'title': _('Editar a %(name)s') % {'name': pet['name']}, 'section': 'profile', 'pet': pet}
    return render(request, 'pet_edit.html', context)


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


# Solo entra quien tiene el permiso del rol Administrator
@login_required
@permission_required('SecurityApp.moderate_content', raise_exception=True)
def admin_panel(request):
    context = {'title': _('Panel de administración')}
    return render(request, 'admin_panel.html', context)


def post_list(request):
    # Filtramos solo los posts publicados y los ordenamos por fecha de publicación descendente
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    # Pasamos los posts al archivo HTML mediante el contexto
    return render(request, 'post_list.html', {'posts': posts})
