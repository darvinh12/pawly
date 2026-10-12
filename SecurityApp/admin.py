from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AuditLog, User


@admin.register(User)
class PawlyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Pawly', {'fields': ('is_banned', 'must_change_password', 'language', 'theme', 'notify_by_email')}),
    )
    list_display = ('username', 'email', 'is_banned', 'is_staff', 'language')
    list_filter = UserAdmin.list_filter + ('is_banned', 'language')


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'action', 'username', 'user', 'ip_address')
    list_filter = ('action',)
    search_fields = ('username',)

    # El registro de auditoría solo se puede leer

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
