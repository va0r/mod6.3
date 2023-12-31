from django.contrib import admin

from mailing.models import Client, MailingSettings, MailingMessage, MailingLog, ClientGroup


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_blocked', 'domain', 'owner',)
    list_filter = ('domain', 'is_blocked', 'owner',)
    search_fields = ('email',)


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('time', 'period', 'status', 'message', 'owner',)
    list_filter = ('period', 'status', 'owner',)
    search_fields = ('message',)


@admin.register(MailingMessage)
class MailingMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'message', 'owner',)
    list_filter = ('owner',)
    search_fields = ('message',)


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('client', 'settings', 'status', 'last_try',)
    list_filter = ('status', 'last_try',)
    ordering = ['-last_try']


@admin.register(ClientGroup)
class ClientGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)
    list_filter = ('owner',)
