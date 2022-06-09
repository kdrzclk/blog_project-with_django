from django.urls import path
from django.contrib.auth import views as auth_views
from .views import profile, register

urlpatterns = [
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),
    path("login/", auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path("loginout/", auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='users/password_reset_email.html'), name="password_reset")

]