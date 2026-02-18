from django.contrib import admin
from web_app.models import MailRecipient

@admin.register(MailRecipient)
class MailRecipientAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'name', 'middle_name', 'email']