from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


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


class MailingAttempt(models.Model):
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, verbose_name='Рассылка')
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Время попытки')
    status = models.CharField(
        max_length=20,
        verbose_name='Статус'
    )
    server_response = models.TextField(blank=True, null=True, verbose_name='Ответ сервера')



class Mailing(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Дата и время начала')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='Статус'
    )

    message = models.ForeignKey(
        'Message',
        on_delete=models.CASCADE,
        verbose_name='Сообщение'
    )

    recipients = models.ManyToManyField(
        'MailRecipient',
        verbose_name='Получатели'
    )

    def update_status(self):
        """Динамическое вычисление и сохранение статуса."""
        now = timezone.now()
        new_status = self.status

        if now < self.start_time:
            new_status = 'created'
        elif self.start_time <= now <= self.end_time:
            new_status = 'started'
        elif now > self.end_time:
            new_status = 'completed'

        if self.status != new_status:
            self.status = new_status
            self.save(update_fields=['status'])

    def clean(self):
        """Валидация полей"""
        if not self.pk and self.start_time < timezone.now():
            raise ValidationError({'start_time': "Время начала не может быть в прошлом."})

        if self.start_time >= self.end_time:
            raise ValidationError("Время начала должно быть строго меньше времени окончания.")

    def __str__(self):
        return f"Рассылка №{self.id} (старт: {self.start_time})"






