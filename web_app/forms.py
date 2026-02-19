from django import forms
from django.urls import reverse_lazy

from .models import MailRecipient
from django.core.exceptions import ValidationError

class MailRecipientForm(forms.ModelForm):
    class Meta:
        model = MailRecipient
        fields = '__all__'
        success_url = reverse_lazy('MailRecipientListView')

    def __init__(self, *args, **kwargs):
        super(MailRecipientForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите имя',
        })

        self.fields['middle_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите отчество',
        })

        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите фамилию',
        })

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите email',
        })

        self.fields['comment'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите описание',
        })

        self.fields['views_counter'].widget.attrs.update({
            'class': 'form-control',
        })


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise ValidationError('Неправильный конец!')
        return email


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        last_name = cleaned_data.get('last_name')

        if name and last_name and name == last_name:
            self.add_error('last_name', 'Неправильная фамилия!')

