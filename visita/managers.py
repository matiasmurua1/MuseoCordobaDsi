from django.db import models

class ReservaVisitaManager(models.Manager):
    def getNumeroReserva(self):
        ultimaReserva = self.all().order_by("numeroReserva").last()
        return ultimaReserva.numeroReserva if ultimaReserva is not None else 0

    def new(self, cantidadAlumnos, duracionEstimada, fechaHoraReserva,
        numeroReserva, exposiciones, sede, estado, guiaAsignado,
        fechaHoraFin, fechaHoraCreacion, escuela):
        nuevaReserva = self.create(
            sede=sede,
            escuela=escuela,
            numeroReserva=numeroReserva,
            cantidadAlumnos=cantidadAlumnos,
            duracionEstimada=duracionEstimada,
            fechaHoraCreacion=fechaHoraCreacion,
            fechaHoraReserva=fechaHoraReserva
        )
        nuevaReserva.exposicion.set(exposiciones)
        nuevaReserva.crearCambioEstado(fechaHoraCreacion, estado)
        nuevaReserva.crearAsignacionGuia(guiaAsignado, fechaHoraReserva, fechaHoraFin)