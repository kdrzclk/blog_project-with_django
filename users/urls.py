from django.urls import path
from django.contrib.auth import views as auth_views
from .views import profile, register

urlpatterns = [
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),

]