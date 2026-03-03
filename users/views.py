import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from users.forms import UserRegisterForm, StyledLoginForm, UserProfileForm
from users.models import User
from config import settings
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib import messages


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/users/confirm_email/{token}/"

        send_mail(
            subject="Подтверждение регистрации",
            message=f"Для подтверждения перейдите по ссылке: {url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)


def confirm_email(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            new_password = secrets.token_hex(8)
            user.set_password(new_password)
            user.save()

            send_mail(
                subject="Восстановление пароля",
                message=f"Ваш новый пароль: {new_password}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            messages.success(request, "Новый пароль отправлен на вашу почту.")
            return redirect(reverse("users:login"))
        else:
            # Если пользователя нет, возвращаем на ту же страницу с ошибкой
            messages.error(request, "Пользователь с таким email не найден.")

    return render(request, "users/reset_password.html")


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = StyledLoginForm

    def get_success_url(self):
        return reverse_lazy("web_app:main")


class UserLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile') # или куда хочешь редиректить
    template_name = 'users/profile_form.html'

    def get_object(self, queryset=None):
        # Это ключевой момент: редактируем именно того, кто залогинен
        return self.request.user
