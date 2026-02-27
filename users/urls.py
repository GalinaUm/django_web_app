from django.urls import path

from users.forms import StyledLoginForm
from users.views import (
    RegisterView,
    confirm_email,
    reset_password,
    UserLoginView,
    UserLogoutView, ProfileUpdateView,
)

app_name = "users"

urlpatterns = [
    path(
        "login/",
        UserLoginView.as_view(
            template_name="users/login.html", form_class=StyledLoginForm
        ),
        name="login",
    ),
    path("logout/", UserLogoutView.as_view(template_name="logout.html"), name="logout"),
    path(
        "register/",
        RegisterView.as_view(template_name="users/register.html"),
        name="register",
    ),
    path("confirm_email/<str:token>/", confirm_email, name="confirm_email"),
    path("reset_password/", reset_password, name="reset_password"),
    path('profile_form/', ProfileUpdateView.as_view(), name='profile_form'),
]
