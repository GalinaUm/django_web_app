from django.core.validators import MaxLengthValidator
from django.db import models


class MailRecipient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя', help_text='Введите ваше имя')
    middle_name = models.CharField(max_length=200, verbose_name='Отчество', help_text='Введите ваше отчество')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия', help_text='Введите вашу фамилию')
    email = models.EmailField(max_length=200, unique=True)
    comment = models.TextField(
        verbose_name='Описание', blank=True, null=True, help_text='Введите комментарий'
    )

    def __str__(self):
        return f'{self.last_name.title()} {self.name.title()} {self.middle_name.title()}: {self.email}'

    views_counter = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        default=0)

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ('last_name', 'name', 'email')


class Message(models.Model):
    subject = models.CharField(
        max_length=70, verbose_name='Тема сообщения', help_text='Напишите тему письма'
    )
    message = models.TextField(
        verbose_name='Сообщение',
        blank=True,
        null=True,
        help_text='Напишите сообщение',
        max_length=5000,
        validators=[MaxLengthValidator(5000)]
    )

    def __str__(self):
        return f'{self.subject.title()} {self.message}'




