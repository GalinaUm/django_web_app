import secrets
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from users.forms import UserRegisterForm
from users.models import User
from config import settings
from django.contrib.auth.views import PasswordResetView

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f'https://{host}/users/confirm-email/{token}/'

        send_mail(
            subject='Подтверждение регистрации',
            message=f'Для подтверждения перейдите по ссылке: {url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        return super().form_valid(form)

def confirm_email(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        new_password = secrets.token_hex(8)
        user.set_password(new_password)
        user.save()

        send_mail(
            subject='Восстановление пароля',
            message=f'Ваш новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return redirect(reverse('users:login'))
    return render(request, 'users/reset_password.html')

 # {% if user.is_authenticated %}
 #    <a href="{% url 'users:logout' %}">Выйти ({{ user.email }})</a>
 #    {% else %}
 #    <a href="{% url 'users:login' %}">Войти</a>
 #    <a href="{% url 'users:register' %}">Регистрация</a>
 #    {% endif %}

# <form method="post">
#     {% csrf_token %}
#     <label for="email">Введите ваш Email для восстановления:</label>
#     <input type="email" name="email" class="form-control" required>
#     <button type="submit" class="btn btn-primary mt-3">Сбросить пароль</button>
# </form>


# <a href="{% url 'users:reset-password' %}">Забыли пароль?</a>
