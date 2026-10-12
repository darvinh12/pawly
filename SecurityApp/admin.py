from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AuditLog, User


admin.site.register(User, UserAdmin)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'action', 'username', 'ip_address')
    list_filter = ('action',)
