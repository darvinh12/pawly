from django.contrib import admin

from .models import Application, Chat, Message, Pet, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'national_id', 'city')
    search_fields = ('full_name', 'user__username', 'national_id')


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'sex', 'owner', 'location', 'for_adoption')
    list_filter = ('species', 'sex', 'for_adoption')
    search_fields = ('name', 'owner__username', 'location')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('pet', 'applicant', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('pet__name', 'applicant__username')


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'application', 'created_at')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'sender', 'text', 'created_at')
    search_fields = ('text', 'sender__username')
