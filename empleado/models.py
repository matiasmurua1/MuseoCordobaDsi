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

class Cargo(models.Model):
    GUIA = "Gu"
    NOMBRE_CHOICES = [
        (GUIA, "Guia"),
    ]

    nombre = models.CharField(u"Nombre", choices=NOMBRE_CHOICES, max_length=2)

    def esGuia(self):
        return self.nombre == self.GUIA

class HorarioEmpleado(models.Model):
    horaIngreso = models.TimeField(u"Hora de ingreso")
    """ Se pone u antes de las comillas del atributo para definir el nombre que ve el usuario."""
    horaSalida = models.TimeField(u"Hora de salida")
    diaSemana = models.ManyToManyField("DiaSemana")

    def dispEnFechaHoraReserva(self):
        """Siempre se pone self como atributo porque pertenece a la misma clase"""
        pass

class DiaSemana(models.Model):
    LUNES = 'Lun'
    MARTES = 'Mar'
    MIERCOLES = 'Mie'
    JUEVES = 'Jue'
    VIERNES = 'Vie'
    SABADO = 'Sab'
    DOMINGO = 'Dom'
    NOMBRE_CHOICES = [
        (LUNES, "Lunes"),
        (MARTES, "Martes"),
        (MIERCOLES, "Miercoles"),
        (JUEVES, "Jueves"),
        (VIERNES, "Viernes"),
        (SABADO, "Sabado"),
        (DOMINGO, "Domingo"),
    ]
    nombre = models.CharField(u"Nombre", choices=NOMBRE_CHOICES, max_length=3)
    """Se define el parametro chocies para limitar que se creen objetos solo
    dentro de un rango de opciones posibles.
    Como el atributo es de tipo string se define el parametro max_length=largo maximo"""

    def esDia(self):
        pass
