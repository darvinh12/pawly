from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from .models import AuditLog, User


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('laura', 'laura@example.com', 'clave12345')

    def test_login_page_is_shown(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bienvenido de vuelta')

    def test_login_with_username_and_with_email(self):
        for name in ('laura', 'laura@example.com'):
            self.client.logout()
            response = self.client.post(reverse('login'), {'username': name, 'password': 'clave12345'})
            self.assertRedirects(response, reverse('home'), fetch_redirect_response=False)

    def test_wrong_password_shows_error_and_is_logged(self):
        response = self.client.post(reverse('login'), {'username': 'laura', 'password': 'mala'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'field__error')
        self.assertTrue(AuditLog.objects.filter(action='login_failed', username='laura').exists())

    def test_banned_user_cannot_log_in(self):
        self.user.is_banned = True
        self.user.save()
        response = self.client.post(reverse('login'), {'username': 'laura', 'password': 'clave12345'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_and_logout_are_logged(self):
        self.client.post(reverse('login'), {'username': 'laura', 'password': 'clave12345'})
        self.client.post(reverse('logout'))
        self.assertEqual(list(AuditLog.objects.order_by('id').values_list('action', flat=True)), ['login', 'logout'])

    def test_without_remember_the_session_ends_with_the_browser(self):
        self.client.post(reverse('login'), {'username': 'laura', 'password': 'clave12345'})
        self.assertTrue(self.client.session.get_expire_at_browser_close())
        self.client.logout()
        self.client.post(reverse('login'), {'username': 'laura', 'password': 'clave12345', 'remember': 'on'})
        self.assertFalse(self.client.session.get_expire_at_browser_close())


class RegisterTests(TestCase):
    data = {'username': 'carlos', 'email': 'carlos@example.com', 'password1': 'clave12345', 'password2': 'clave12345'}

    def test_register_creates_user_with_member_role_and_logs_in(self):
        response = self.client.post(reverse('register'), self.data)
        self.assertRedirects(response, reverse('profile_form'), fetch_redirect_response=False)
        user = User.objects.get(username='carlos')
        self.assertTrue(user.groups.filter(name='Member').exists())
        self.assertEqual(user.language, 'es')
        self.assertTrue(AuditLog.objects.filter(action='register', user=user).exists())
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    def test_password_needs_a_number(self):
        response = self.client.post(reverse('register'), dict(self.data, password1='sinnumeros', password2='sinnumeros'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'al menos un número')
        self.assertFalse(User.objects.filter(username='carlos').exists())

    def test_email_must_be_unique(self):
        User.objects.create_user('otro', 'carlos@example.com', 'clave12345')
        response = self.client.post(reverse('register'), self.data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='carlos').exists())


class RolesTests(TestCase):
    def test_roles_exist_with_permissions(self):
        admin_role = Group.objects.get(name='Administrator')
        codenames = set(admin_role.permissions.values_list('codename', flat=True))
        self.assertTrue({'ban_user', 'moderate_content', 'view_auditlog', 'change_user'} <= codenames)
        self.assertEqual(Group.objects.get(name='Member').permissions.count(), 0)

    def test_administrator_role_gives_permissions(self):
        user = User.objects.create_user('admin1', 'admin1@example.com', 'clave12345')
        self.assertFalse(user.has_perm('SecurityApp.ban_user'))
        user.groups.add(Group.objects.get(name='Administrator'))
        user = User.objects.get(pk=user.pk)
        self.assertTrue(user.has_perm('SecurityApp.ban_user'))


class LanguageTests(TestCase):
    def test_user_language_is_used(self):
        User.objects.create_user('john', 'john@example.com', 'clave12345', language='en')
        self.client.login(username='john', password='clave12345')
        response = self.client.get(reverse('adoption_feed'))
        self.assertContains(response, 'lang="en"')
        self.assertContains(response, 'Pets near Chacao, Caracas')
        self.assertContains(response, 'Skip to content')

    def test_default_language_is_spanish(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'lang="es"')
        self.assertContains(response, 'Saltar al contenido')

    def test_set_language_changes_the_page(self):
        self.client.post('/i18n/setlang/', {'language': 'en', 'next': '/login/'})
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'Welcome back')

    def test_logged_in_user_changes_language_and_it_is_saved(self):
        user = User.objects.create_user('ana', 'ana@example.com', 'clave12345')
        self.client.login(username='ana', password='clave12345')
        self.client.post('/i18n/setlang/', {'language': 'en', 'next': '/adoption/'})
        user.refresh_from_db()
        self.assertEqual(user.language, 'en')
        self.assertContains(self.client.get(reverse('adoption_feed')), 'Skip to content')
        self.client.post('/i18n/setlang/', {'language': 'es', 'next': '/adoption/'})
        self.assertContains(self.client.get(reverse('adoption_feed')), 'Saltar al contenido')

    def test_invalid_language_is_not_saved(self):
        user = User.objects.create_user('ana', 'ana@example.com', 'clave12345')
        self.client.login(username='ana', password='clave12345')
        self.client.post('/i18n/setlang/', {'language': 'xx', 'next': '/'})
        user.refresh_from_db()
        self.assertEqual(user.language, 'es')


class ScreensOfAccessTests(TestCase):
    def test_profile_step_needs_login_and_password_reset_is_public(self):
        self.assertRedirects(self.client.get(reverse('profile_form')), f"{reverse('login')}?next={reverse('profile_form')}",
                             fetch_redirect_response=False)
        response = self.client.get(reverse('password_reset'))
        self.assertContains(response, 'Recuperar contraseña')

    def test_register_flow_ends_in_the_profile_step_and_then_home(self):
        data = {'username': 'carlos', 'email': 'carlos@example.com', 'password1': 'clave12345', 'password2': 'clave12345'}
        self.client.post(reverse('register'), data)
        response = self.client.get(reverse('profile_form'))
        self.assertContains(response, 'Paso 2 de 2')
        self.assertContains(response, reverse('home'))

    def test_settings_screen_changes_the_language(self):
        User.objects.create_user('ana', 'ana@example.com', 'clave12345')
        self.client.login(username='ana', password='clave12345')
        response = self.client.get(reverse('account_settings'))
        self.assertContains(response, 'action="/i18n/setlang/"')
        self.assertContains(response, 'value="es" checked')
        self.client.post('/i18n/setlang/', {'language': 'en', 'next': reverse('account_settings')})
        response = self.client.get(reverse('account_settings'))
        self.assertContains(response, 'value="en" lang="en" checked')
        self.assertContains(response, 'Appearance and language')
