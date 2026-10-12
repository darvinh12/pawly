from django.contrib.auth.models import Group
from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import reverse

from SecurityApp.models import User

# Todas las pantallas que necesitan haber iniciado sesión: nombre de la ruta, argumentos y plantilla
PRIVATE_SCREENS = [
    ('home', [], 'home.html'),
    ('search', [], 'search.html'),
    ('adoption_feed', [], 'adoption_feed.html'),
    ('pet_detail', [1], 'pet_detail.html'),
    ('application_form', [1], 'application_form.html'),
    ('chat_list', [], 'chat_list.html'),
    ('chat_detail', [1], 'chat_detail.html'),
    ('notifications', [], 'notifications.html'),
    ('my_profile', [], 'my_profile.html'),
    ('account_settings', [], 'account_settings.html'),
    ('pet_profile', [1], 'pet_profile.html'),
    ('pet_edit', [1], 'pet_edit.html'),
    ('user_profile', [1], 'user_profile.html'),
    ('post_create', [], 'post_create.html'),
    ('post_detail', [1], 'post_detail.html'),
    ('report', [1], 'report.html'),
    ('profile_form', [], 'profile_form.html'),
]


class ScreensTests(TestCase):
    def setUp(self):
        User.objects.create_user('laura', 'laura@example.com', 'clave12345')

    def log_in(self):
        self.client.login(username='laura', password='clave12345')

    def test_screens_need_login(self):
        for name, args, template in PRIVATE_SCREENS:
            url = reverse(name, args=args)
            response = self.client.get(url)
            self.assertRedirects(response, f"{reverse('login')}?next={url}", fetch_redirect_response=False)

    def test_every_screen_renders_with_its_template_and_base(self):
        self.log_in()
        for name, args, template in PRIVATE_SCREENS:
            response = self.client.get(reverse(name, args=args))
            self.assertEqual(response.status_code, 200, name)
            self.assertTemplateUsed(response, template)
            self.assertTemplateUsed(response, 'base.html')
        for name, template in [('login', 'login.html'), ('register', 'register.html'), ('password_reset', 'password_reset.html')]:
            self.client.logout()
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, 200, name)
            self.assertTemplateUsed(response, template)
            self.assertTemplateUsed(response, 'base.html')

    def test_pages_have_no_template_leftovers_or_broken_attributes(self):
        from html.parser import HTMLParser

        class Checker(HTMLParser):
            def __init__(self):
                super().__init__()
                self.bad = []

            def handle_starttag(self, tag, attrs):
                for name, value in attrs:
                    if value and ('\\' in value or '{%' in value or '{{' in value):
                        self.bad.append(f'{tag} {name}={value}')

        self.log_in()
        pages = [reverse(name, args=args) for name, args, template in PRIVATE_SCREENS]
        for language in ('es', 'en'):
            self.client.post('/i18n/setlang/', {'language': language, 'next': '/'})
            for url in pages:
                html = self.client.get(url).content.decode()
                self.assertNotIn('{%', html, url)
                self.assertNotIn('%(', html, url)
                checker = Checker()
                checker.feed(html)
                self.assertEqual(checker.bad, [], url)

    def test_app_screens_extend_base_app(self):
        self.log_in()
        for name, args, template in PRIVATE_SCREENS:
            if name == 'profile_form':
                continue
            self.assertTemplateUsed(self.client.get(reverse(name, args=args)), 'base_app.html')

    def test_screens_have_title_and_section_in_the_menu(self):
        self.log_in()
        expected = {'home': 'Inicio · Pawly', 'chat_list': 'Mensajes · Pawly', 'notifications': 'Notificaciones · Pawly',
                    'my_profile': 'Mi perfil · Pawly', 'account_settings': 'Ajustes · Pawly',
                    'post_create': 'Nueva publicación · Pawly', 'search': 'Resultados para «luna» · Pawly'}
        for name, title in expected.items():
            self.assertContains(self.client.get(reverse(name)), f'<title>{title}</title>')
        # La pantalla de inicio marca Inicio como la sección actual
        home = self.client.get(reverse('home')).content.decode()
        self.assertIn(f'href="{reverse("home")}" aria-current="page"', home)

    def test_home_is_the_start_page(self):
        self.log_in()
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Luna cumplió 3 años hoy')
        self.assertContains(response, 'has-header-mobile')

    def test_feed_lists_the_pets_and_links_to_their_detail(self):
        self.log_in()
        response = self.client.get(reverse('adoption_feed'))
        for name in ('Toby', 'Nala', 'Rocky', 'Kira', 'Bruno', 'Coco', 'Simón', 'Max'):
            self.assertContains(response, name)
        self.assertContains(response, '/media/pets/d1.jpg')
        self.assertContains(response, '/static/css/pawly.css')
        self.assertContains(response, f'href="{reverse("pet_detail", args=[2])}"')

    def test_pet_detail_shows_the_data_of_each_pet(self):
        self.log_in()
        toby = self.client.get(reverse('pet_detail', args=[1]))
        self.assertContains(toby, '<title>Toby · Adopción · Pawly</title>')
        self.assertContains(toby, 'Se abrirá un chat con Luis.')
        self.assertContains(toby, reverse('application_form', args=[1]))
        nala = self.client.get(reverse('pet_detail', args=[2]))
        self.assertContains(nala, 'Sobre Nala')
        self.assertContains(nala, 'Gato · Atigrada')
        self.assertContains(nala, 'Lunita Rescates')
        self.assertContains(nala, reverse('application_form', args=[2]))

    def test_static_files_and_media_exist(self):
        for path in ('css/pawly.css', 'js/pawly.js', 'img/logo-full.png', 'img/logo-mark.png', 'img/logo-word.png',
                     'img/hero.jpg', 'img/icons/search.svg', 'img/icons/paw.svg', 'img/icons/logout.svg'):
            self.assertIsNotNone(finders.find(path), path)

    def test_every_static_file_used_by_the_screens_exists(self):
        import re
        self.log_in()
        paths = set()
        for name, args, template in PRIVATE_SCREENS:
            html = self.client.get(reverse(name, args=args)).content.decode()
            paths.update(re.findall(r'(?:src|href)="/static/([^"#?]+)', html))
        self.client.logout()
        for name in ('login', 'register', 'password_reset'):
            html = self.client.get(reverse(name)).content.decode()
            paths.update(re.findall(r'(?:src|href)="/static/([^"#?]+)', html))
        self.assertGreater(len(paths), 20)
        for path in sorted(paths):
            self.assertIsNotNone(finders.find(path), path)

    def test_application_form_shows_the_pet_and_the_owner(self):
        self.log_in()
        response = self.client.get(reverse('application_form', args=[1]))
        self.assertContains(response, 'Postularte para adoptar a Toby')
        self.assertContains(response, 'Mensaje para Luis')
        self.assertContains(response, 'Chacao, Caracas · a 2 km de ti')
        self.assertContains(response, '<header class="app-header" inert>', html=False)
        self.assertContains(response, reverse('pet_detail', args=[1]))

    def test_application_with_message_goes_to_the_pet_with_the_sent_notice(self):
        self.log_in()
        response = self.client.post(reverse('application_form', args=[1]), {'message': 'Hola, quiero adoptar'})
        self.assertRedirects(response, reverse('pet_detail', args=[1]) + '?postulacion=enviada',
                             fetch_redirect_response=False)

    def test_application_without_message_shows_the_error(self):
        self.log_in()
        response = self.client.post(reverse('application_form', args=[1]), {'message': '   '})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Escribe un mensaje para el dueño</p>')

    def test_unknown_items_are_404(self):
        self.log_in()
        for name in ('application_form', 'pet_detail', 'pet_profile', 'pet_edit', 'chat_detail', 'user_profile',
                     'post_detail', 'report'):
            self.assertEqual(self.client.get(reverse(name, args=[99])).status_code, 404, name)

    def test_pet_profile_content(self):
        self.log_in()
        response = self.client.get(reverse('pet_profile', args=[1]))
        self.assertContains(response, 'Sobre Mía')
        self.assertContains(response, 'Ocumare del Tuy, Miranda')
        self.assertContains(response, '<title>Mía · Mis mascotas · Pawly</title>')
        self.assertContains(response, reverse('pet_edit', args=[1]))

    def test_logout_link_ends_the_session(self):
        self.log_in()
        self.assertContains(self.client.get(reverse('account_settings')), f'href="{reverse("logout")}"')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertRedirects(self.client.get(reverse('home')), f"{reverse('login')}?next=/", fetch_redirect_response=False)


class AdminPanelTests(TestCase):
    def test_only_the_administrator_role_enters(self):
        user = User.objects.create_user('ana', 'ana@example.com', 'clave12345')
        self.client.login(username='ana', password='clave12345')
        self.assertEqual(self.client.get(reverse('admin_panel')).status_code, 403)
        user.groups.add(Group.objects.get(name='Administrator'))
        response = self.client.get(reverse('admin_panel'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_admin.html')
        self.assertContains(response, 'Panel de administración')
        self.assertContains(response, 'layout-admin')

    def test_anonymous_goes_to_login(self):
        url = reverse('admin_panel')
        self.assertRedirects(self.client.get(url), f"{reverse('login')}?next={url}", fetch_redirect_response=False)
