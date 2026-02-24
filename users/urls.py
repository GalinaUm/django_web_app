from django.urls import path

from users.forms import StyledLoginForm
from users.views import (
    RegisterView,
    confirm_email,
    reset_password,
    UserLoginView,
    UserLogoutView,
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
    path("confirm-email/<str:token>/", confirm_email, name="confirm-email"),
    path("reset-password/", reset_password, name="reset-password"),
]
