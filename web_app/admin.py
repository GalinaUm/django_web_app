from django.contrib import admin
from web_app.models import MailRecipient, Message


@admin.register(MailRecipient)
class MailRecipientAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'name', 'middle_name', 'email']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'message']