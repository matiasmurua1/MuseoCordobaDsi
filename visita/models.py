from django.db import models
from django.utils.timezone import timedelta 

from empleado.models import Empleado
from exposicion.models import Exposicion, Sede
from .managers import ReservaVisitaManager

# Create your models here.
class Escuela(models.Model):
    nombre = models.CharField(u"Nombre", max_length=64, unique=True)

    def __str__(self):
        return self.nombre

class TipoVisita(models.Model):
    COMPLETA = 0
    POR_EXPOSICION = 1
    NOMBRE_CHOICES = [
        (COMPLETA, "Completa"),
        (POR_EXPOSICION, "Por exposicion")
    ]

    nombre = models.PositiveSmallIntegerField(u"Nombre", choices=NOMBRE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_nombre_display()

    def esPorExposicion(self):
        return self.nombre == self.POR_EXPOSICION
    
    def esCompleta(self):
        return self.nombre == self.COMPLETA

    def get_nombre(self):
        return (self.nombre, self.get_nombre_display())

class Estado(models.Model):
    PENDIENTE_CONFIRMACION = 1
    PENDIENTE_ASIGNACION_DEPOSITO = 2
    NOMBRE_CHOICES = [
        (PENDIENTE_CONFIRMACION, "Pendiente de confirmacion"),
        (PENDIENTE_ASIGNACION_DEPOSITO, "Pendiente de asignacion a deposito")
    ]

    RESERVA = 1
    OBRA = 2
    AMBITO_CHOICES = [
        (RESERVA, "Reserva"),
        (OBRA, "Obra")
    ]

    ambito = models.PositiveSmallIntegerField(u"Ambito", choices=AMBITO_CHOICES)
    nombre = models.PositiveSmallIntegerField(u"Nombre", choices=NOMBRE_CHOICES)

    def __str__(self):
        return f'{self.get_ambito_display()}: {self.get_nombre_display()}'

    def esAmbitoReserva(self):
        return self.ambito == self.RESERVA

    def esPendienteDeConfirmacion(self):
        return self.nombre == self.PENDIENTE_CONFIRMACION

class CambioEstado(models.Model):
    fechaHoraInicio = models.DateTimeField(u"Fecha hora de inicio")
    estado = models.ForeignKey("Estado", on_delete=models.PROTECT)
    reservaVisita = models.ForeignKey("ReservaVisita", on_delete=models.PROTECT, related_name="cambioEstado")

class ReservaVisita(models.Model):
    cantidadAlumnos = models.PositiveIntegerField(u"Cantidad de alumnos")
    duracionEstimada = models.PositiveIntegerField(u"Duracion estimada", help_text="Duracion expresada en minutos")
    fechaHoraCreacion = models.DateTimeField(u"Fecha y hora de creacion")
    fechaHoraReserva = models.DateTimeField(u"Fecha y hora de reserva")
    numeroReserva = models.PositiveBigIntegerField(u"Numero reserva", unique=True, primary_key=True)
    exposicion = models.ManyToManyField(Exposicion)
    sede = models.ForeignKey(Sede, on_delete=models.PROTECT, related_name="reserva")
    escuela = models.ForeignKey("Escuela", on_delete=models.PROTECT)
    
    objects = ReservaVisitaManager()

    def crearAsignacionGuia(self, guiasAsignados, fechaHoraReserva, fechaHoraFin):
        for guia in guiasAsignados:
            self.asignacionGuia.create(
                guiaAsignado=guia, 
                fechaHoraInicio=fechaHoraReserva,
                fechaHoraFin=fechaHoraFin)

    def crearCambioEstado(self, fechaHora, estado):
        self.cambioEstado.create(fechaHoraInicio=fechaHora, estado=estado)

    def obtenerAlumnosEnReserva(self, fechaHoraDesde, fechaHoraHasta):
        reservaHasta = self.fechaHoraReserva + timedelta(minutes=self.duracionEstimada)
        if (fechaHoraDesde <= self.fechaHoraReserva and self.fechaHoraReserva < fechaHoraHasta) \
            or (fechaHoraDesde > self.fechaHoraReserva and (reservaHasta <= fechaHoraHasta or reservaHasta > fechaHoraHasta)):
            return self.cantidadAlumnos
        return 0

class AsignacionVisita(models.Model):
    fechaHoraFin = models.DateTimeField(u"Fecha y hora de fin")
    fechaHoraInicio = models.DateTimeField(u"Fecha y hora de inicio")
    reservaVisita = models.ForeignKey("ReservaVisita", related_name="asignacionGuia", on_delete=models.PROTECT)
    guiaAsignado = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name="asignacionVisita")

    def esAsignacionParaFechaHora(self, fechaHoraDesde, fechaHoraHasta):
        return (self.fechaHoraInicio >= fechaHoraDesde and self.fechaHoraInicio <= fechaHoraHasta) or \
            (self.fechaHoraFin >= fechaHoraDesde and self.fechaHoraFin <= fechaHoraHasta) or \
            (self.fechaHoraInicio <= fechaHoraDesde and self.fechaHoraFin >= fechaHoraHasta)        
