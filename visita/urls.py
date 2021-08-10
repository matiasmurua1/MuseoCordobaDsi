from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm

from . import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="login.html", authentication_form=AuthenticationForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="visita:index"), name="logout"),
    path("registrar/visita/", views.registrarReservaVisitaGuiada, name="registrar_visita"),
    path("tomar/reg/reserva/visita/", views.tomarRegReservaVisitaGuiada, name="tomarRegReservaVisitaGuiada"),
    path("tomar/escuela/", views.tomarSeleccionEscuela, name="tomarSeleccionEscuela"),
    path("tomar/cantidad/visitantes/", views.tomarCantVisitantes, name="tomarCantVisitantes"),
    path("tomar/seleccion/sede/", views.tomarSeleccionSede, name="tomarSeleccionSede"),
    path("tomar/seleccion/tipo/visita/", views.tomarSeleccionTipoVisita, name="tomarSeleccionTipoVisita"),
    path("tomar/fechaHora/reserva/", views.tomarFechaHoraReserva, name="tomarFechaHoraReserva"),
    path("tomar/guias/", views.tomarGuias, name="tomarGuias"),
    path("tomar/registrar/visita/", views.registrarVisita, name="registrarVisita"),
    path("", views.index, name="index"),
]
