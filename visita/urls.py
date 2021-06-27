from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm

from . import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="login.html", authentication_form=AuthenticationForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="visita:index"), name="logout"),
    path("", views.index, name="index"),
]
