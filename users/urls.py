from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.views import RegisterView, confirm_email, reset_password

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-email/<str:token>/', confirm_email, name='confirm-email'),
    path('reset-password/', reset_password, name='reset-password'),
]
