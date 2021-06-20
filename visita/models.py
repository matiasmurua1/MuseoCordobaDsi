from django.db import models
from empleado.models import Empleado
from exposicion.models import Exposicion, Sede

# Create your models here.
class Escuela(models.Model):
    nombre = models.CharField(u"Nombre", max_length=64)

class TipoVisita(models.Model):
    nombre = models.CharField(u"Nombre", max_length=64)

class Estado(models.Model):
    PENDIENTE_CONFIRMACION = 1
    NOMBRE_CHOICES = [
        (PENDIENTE_CONFIRMACION, "Pendiente de confirmacion")
    ]

    RESERVA = 1
    AMBITO_CHOICES = [
        (RESERVA, "Reserva")
    ]

    nombre = models.PositiveSmallIntegerField(u"Nombre", choices=NOMBRE_CHOICES)
    ambito = models.PositiveSmallIntegerField(u"Ambito", choices=AMBITO_CHOICES)

    def esAmbitoReserva(self):
        return self.ambito == self.AMBITO_CHOICES

    def esPendienteDeConfirmacion(self):
        return self.nombre == self.PENDIENTE_CONFIRMACION

class CambioEstado(models.Model):
    fechaHoraInicio = models.DateTimeField(u"Fecha hora de inicio")
    estado = models.ForeignKey("Estado", on_delete=models.PROTECT)

class ReservaVisita(models.Model):
    cantidadAlumnos = models.PositiveIntegerField(u"Cantidad de alumnos")
    duracionEstimada = models.PositiveIntegerField(u"Duracion estimada", help_text="Duracion expresada en minutos")
    fechaHoraCreacion = models.DateTimeField(u"Fecha y hora de creacion")
    fechaHoraReserva = models.DateTimeField(u"Fecha y hora de reserva")
    numeroReserva = models.PositiveBigIntegerField(u"Numero reserva", unique=True, primary_key=True)
    exposicion = models.ManyToManyField(Exposicion)
    sede = models.ForeignKey(Sede, on_delete=models.PROTECT)

    def getNumeroReserva(self):
        pass

    def crearAsignacionGuia(self):
        pass

    def crearCambioEstado(self):
        pass

    def obtenerAlumnosEnReserva(self):
        pass

class AsignacionVisita(models.Model):
    fechaHoraFin = models.DateTimeField(u"Fecha y hora de fin")
    fechaHoraInicio = models.DateTimeField(u"Fecha y hora de inicio")
    reservaVisita = models.ForeignKey("ReservaVisita", related_name="asignacionGuia", on_delete=models.PROTECT)
    guiaAsignado = models.ForeignKey(Empleado, on_delete=models.PROTECT)

    def esAsignacionParaFechaHora(self):
        pass
