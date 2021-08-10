from django.db import models
from django.contrib.auth.models import User
""" Import para apuntar a la clase User de Django"""

# Create your models here.
class Empleado(models.Model):
    # La clase Empleado hereda los comportamientos y atributos de la clase Model
    # Que son necesarios para convertir un objeto en registro de base de datos
    # Y viceversa. Es decir el paquete models es parte del framework de
    # de persistencia de Django. Todas las clases que se generan en el archivo
    # models.py que tienen persistencia de datos, heredan de models.Model


    """ Se pone como primer atributo la clase destino del puntero.
    Va entre comillas porque el atributo es de tipo puntero"""


    cargo = models.ForeignKey("Cargo", on_delete=models.PROTECT)
    """Se usa ForeignKey siempre que en el diagrama de clases la  multiplicidad de la
    flecha de vuelta sea 1 a muchos. 
    Al ser una relacion fuerte, se debe definir que ocurre cuando se elimina un
    objeto de la clase a la que apunta. Se debe prevenir
    que se borre el objeto de la base de datos definiendo el parametro on_delete=models.PROTECT"""

    horarioEmpleado = models.ManyToManyField("HorarioEmpleado")
    """ Como en el diagrama de clases la relacion de ida es 0..* y la de vuelta tambien
    entonces no necesita que se le defina el parametro on_delete"""

    usuario = models.OneToOneField(User, on_delete=models.PROTECT)
    """ Como la clase a la que apunta no esta dentro de la misma app, no se usan comillas.
    Se tiene que importar desde la app donde se encuentra.
    Se cambia la punta de flecha del diagrama para poder aprovechar todas las funcionalidades
    de autenticacion y de sesion que vienen por defecto con django"""

    sede = models.ForeignKey("exposicion.Sede", on_delete=models.PROTECT, related_name="empleado")
    nombre = models.CharField(u"Nombre", max_length=128)

    def getGuiaDispEnHorario(self, fechaHoraDesde, fechaHoraHasta):
        if self.cargo.esGuia():
            for horario in self.horarioEmpleado.all():
                if horario.dispEnFechaHoraReserva(fechaHoraDesde, fechaHoraHasta):
                    for asignacion in self.asignacionVisita.all():
                        if asignacion.esAsignacionParaFechaHora(fechaHoraDesde, fechaHoraHasta):
                            return None
                    return {"id":self.pk, "nombre":self.nombre}
        return None

class Cargo(models.Model):
    GUIA = "Gu"
    RESPONSABLE_VISITAS = "RV"
    NOMBRE_CHOICES = [
        (GUIA, "Guia"),
        (RESPONSABLE_VISITAS, "Responsable de visitas"),
    ]

    nombre = models.CharField(u"Nombre", choices=NOMBRE_CHOICES, max_length=2, unique=True)

    def esGuia(self):
        return self.nombre == self.GUIA
    
    def __str__(self):
        return self.get_nombre_display()

class HorarioEmpleado(models.Model):
    horaIngreso = models.TimeField(u"Hora de ingreso")
    """ Se pone u antes de las comillas del atributo para definir el nombre que ve el usuario."""
    horaSalida = models.TimeField(u"Hora de salida")
    diaSemana = models.ManyToManyField("DiaSemana")

    def dispEnFechaHoraReserva(self, fechaHoraDesde, fechaHoraHasta):
        """Siempre se pone self como atributo porque pertenece a la misma clase"""
        horaDesde = fechaHoraDesde.time()
        horaHasta = fechaHoraHasta.time()
        for dia in self.diaSemana.all():
            if dia.esDia(fechaHoraDesde) and \
                self.horaIngreso <= horaDesde and \
                horaDesde < self.horaSalida and \
                self.horaIngreso < horaHasta and \
                horaHasta <= self.horaSalida:
                return True
        return False

class DiaSemana(models.Model):
    LUNES = 0
    MARTES = 1
    MIERCOLES = 2
    JUEVES = 3
    VIERNES = 4
    SABADO = 5
    DOMINGO = 6
    NOMBRE_CHOICES = [
        (LUNES, "Lunes"),
        (MARTES, "Martes"),
        (MIERCOLES, "Miercoles"),
        (JUEVES, "Jueves"),
        (VIERNES, "Viernes"),
        (SABADO, "Sabado"),
        (DOMINGO, "Domingo"),
    ]
    nombre = models.PositiveSmallIntegerField(u"Nombre", choices=NOMBRE_CHOICES, primary_key=True)
    """Se define el parametro chocies para limitar que se creen objetos solo
    dentro de un rango de opciones posibles.
    Como el atributo es de tipo string se define el parametro max_length=largo maximo"""

    def __str__(self):
        return self.get_nombre_display()

    def esDia(self, date):
        return date.weekday() == self.nombre
