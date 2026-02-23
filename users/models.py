from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)

    avatar = models.ImageField(upload_to='users/avatars/%Y/%m', verbose_name='Аватар', blank=True, null=True)
    phone = models.CharField(max_length=35, verbose_name='Телефон', blank=True, null=True)
    country = models.CharField(max_length=50, verbose_name='Страна', blank=True, null=True)

    token = models.CharField(max_length=100, verbose_name='Токен подтверждения', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


