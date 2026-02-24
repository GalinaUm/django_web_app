from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ("email",)


@admin.register(User)
class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm  # Форма редактирования
    add_form = MyUserCreationForm
    # Указываем, какие поля отображать в списке пользователей
    list_display = ('email', 'phone', 'country', 'is_staff')

    # Убираем username из фильтров и поиска
    search_fields = ('email', 'phone')
    ordering = ('email',)

    # ОЧЕНЬ ВАЖНО: Переопределяем наборы полей (fieldsets), чтобы исключить 'username'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('avatar', 'phone', 'country', 'token')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Также нужно убрать username из формы создания пользователя, если вы её используете
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password'),
        }),
    )
