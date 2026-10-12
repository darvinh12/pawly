from django.apps import AppConfig
from django.db.models.signals import post_migrate

# Los roles son grupos de Django. Cada rol tiene los permisos de esta lista
ROLES = {
    'Administrator': ['view_user', 'add_user', 'change_user', 'delete_user',
                      'ban_user', 'moderate_content', 'view_auditlog'],
    'Member': [],
}


def create_roles(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission

    for name, codenames in ROLES.items():
        group, _ = Group.objects.get_or_create(name=name)
        group.permissions.set(Permission.objects.filter(
            content_type__app_label='SecurityApp', codename__in=codenames))


class SecurityappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SecurityApp'

    def ready(self):
        # Se importan las señales para que queden conectadas (registro de auditoría)
        from . import signals  # noqa: F401

        post_migrate.connect(create_roles, sender=self, dispatch_uid='security_create_roles')
