from django.contrib import admin

# Register your models here.
from django.contrib import admin

from mailing_services.models import Client, Message, Mailing, MailingLogs


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'comments',)
    search_fields = ('name', 'email',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('header', 'body',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('time', 'create_date', 'regularity', 'status', 'get_clients', 'message',)


@admin.register(MailingLogs)
class MailingLogsAdmin(admin.ModelAdmin):
    list_display = ('status', 'data_time', 'server_response', 'mailing',)
