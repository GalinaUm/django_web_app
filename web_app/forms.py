from django import forms
from django.urls import reverse_lazy

from .models import MailRecipient, Message, Mailing
from django.core.exceptions import ValidationError


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class MailRecipientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailRecipient
        fields = "__all__"
        success_url = reverse_lazy("MailRecipientListView")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@gmail.com"):
            raise ValidationError("Неправильный конец!")
        return email

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        last_name = cleaned_data.get("last_name")

        if name and last_name and name == last_name:
            self.add_error("last_name", "Неправильная фамилия!")


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"
        success_url = reverse_lazy("MessageListView")


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = "__all__"
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }
        success_url = reverse_lazy("MailingListView")
