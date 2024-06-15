from django.urls import path
from . import views

urlpatterns = [
    path("me/", views.home, name="me"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("settings/", views.settings, name="settings")
]
