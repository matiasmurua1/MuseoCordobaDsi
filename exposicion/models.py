from django.db import models

# Create your models here.
class Sede(models.Model):
    cantMaximaVisita = models.PositiveIntegerField(u"Cantidad maxima de visitantes")
    cantMaximaPorGuia = models.PositiveIntegerField(u"Cantidad maxima por guia")
    """ El atributo es de tipo int que solo acepta valores positivos"""
    nombre = models.CharField(u"Nombre", max_length=64, unique=True)

    def __str__(self):
        return self.nombre
    
    @property
    def horaApertura(self):
        apertura = ""
        for horario in self.horario.all():
            apertura += f'{horario.horaApertura}'
        return apertura

    @property
    def horaCierre(self):
        cierre = ""
        for horario in self.horario.all():
            cierre += f'{horario.horaCierre} ({horario.dias})'
        return cierre

    def buscarDuracionExposiciones(self, exposiciones, completa=False, porExposicion=False):
        duracion = 0
        for exposicion in exposiciones:
            if porExposicion:
                duracion += exposicion.buscarDuracionExtObra()
                continue
            if completa:
                duracion += exposicion.buscarDuracionResObra()
                continue
        return duracion

    def buscarExposiciones(self, hoy, esCompleta=False):
        exposiciones = []
        for exposicion in self.exposicion.all():
            detalles = exposicion.getTempVigentes(hoy)
            if detalles is not None:
                exposiciones.append(detalles)
            
            if esCompleta:
                detalles = exposicion.getPermanentes()
                if detalles is not None:
                    exposiciones.append(detalles)
            
        return exposiciones

    def buscarResParaFechaHora(self, fechaHoraReserva, fechaHoraReservaHasta):
        cantidadVisitantes = 0
        for reserva in self.reserva.all():
            cantidadVisitantes += reserva.obtenerAlumnosEnReserva(
                fechaHoraReserva, 
                fechaHoraReservaHasta)
        return cantidadVisitantes

class PublicoDestino(models.Model):
    nombre = models.CharField(u"Nombre", max_length=64)

    def __str__(self):
        return self.nombre

class TipoExposicion(models.Model):
    TEMPORAL = 1
    PERMANENTE = 2
    NOMBRE_CHOICES = [
        (TEMPORAL, "Temporal"),
        (PERMANENTE, "Permanente"),
    ]

    nombre = models.PositiveSmallIntegerField(u"Nombre", choices=NOMBRE_CHOICES, primary_key=True)
    descripcion = models.CharField(u"Descripcion", max_length=255, null=True)

    def __str__(self):
        return self.get_nombre_display()

    def esTemporal(self):
        return self.nombre == self.TEMPORAL
    
    def esPermanente(self):
        return self.nombre == self.PERMANENTE

class HorarioSede(models.Model):
    horaApertura = models.TimeField(u"Hora apertura")
    horaCierre = models.TimeField(u"Hora cierre")
    sede = models.ForeignKey("Sede", on_delete=models.CASCADE, related_name="horario")
    diaSemana = models.ManyToManyField("empleado.DiaSemana")

    def conocerDiaSemana(self):
        return self.diaSemana.all()

    @property
    def dias(self):
        diaString = ""
        for dia in self.conocerDiaSemana():
            diaString += f'{dia.get_nombre_display()}, '
        diaString = diaString[:-2]
        return diaString

class Exposicion(models.Model):
    fechaFin = models.DateField(u"Fecha fin", null=True, blank=True)
    fechaInicio = models.DateField(u"Fecha inicio", null=True, blank=True)
    fechaFinReplanificada = models.DateField(u"Fecha fin replanificada", null=True, blank=True)
    """Parametro null=True para permitir guardar un atributo con valor nulo"""
    fechaInicioReplanificada = models.DateField(u"Fecha inicio replanificada", null=True, blank=True)
    horaApertura = models.TimeField(u"Hora apertura", null=True, blank=True)
    horaCierre = models.TimeField(u"Hora cierre", null=True, blank=True)
    nombre = models.CharField(u"Nombre", max_length=64)
    publicoDestino = models.ManyToManyField("PublicoDestino")
    tipoExposicion = models.ForeignKey("TipoExposicion", on_delete=models.PROTECT)
    sede = models.ForeignKey("Sede", on_delete=models.PROTECT, related_name="exposicion")

    def __str__(self):
        return self.nombre

    def buscarDuracionExtObra(self):
        duracion = 0
        for detalle in self.detalleExposicion.all():
            duracion += detalle.buscarDuracionExtObra()
        return duracion

    def buscarDuracionResObra(self):
        duracion = 0
        for detalle in self.detalleExposicion.all():
            duracion += detalle.buscarDuracionResObra()
        return duracion

    def getHorarioHabilitado(self):
        if (self.tipoExposicion.esTemporal()):
            return {
                "horaApertura": self.horaApertura,
                "horaCierre": self.horaCierre
            }
        if (self.tipoExposicion.esPermanente()):
            return {
                "horaApertura": self.sede.horaApertura,
                "horaCierre": self.sede.horaCierre,
            }

    def getTempVigentes(self, hoy):
        if (not self.tipoExposicion.esTemporal()) or \
        (self.fechaFin < hoy or \
        (self.fechaFinReplanificada is not None and self.fechaFinReplanificada < hoy)):
            return None
        return self.buildDetailsDictionary()
        

    def buildDetailsDictionary(self):
        publicoDestino = ""
        for publico in self.publicoDestino.all():
            publicoDestino += f'{publico.nombre} - '

        publicoDestino = publicoDestino[:-3]
        
        return {
            "id": self.pk,
            "nombre": self.nombre,
            "horarioHabilitado": self.getHorarioHabilitado(),
            "publicoDestino": publicoDestino
        }
    
    def getPermanentes(self):
        if (self.tipoExposicion.esPermanente()):
            return self.buildDetailsDictionary()
        return None

class DetalleExposicion(models.Model):
    obra = models.ForeignKey("Obra", on_delete=models.PROTECT)
    exposicion = models.ForeignKey("Exposicion", on_delete=models.PROTECT, related_name="detalleExposicion")

    def buscarDuracionExtObra(self):
        return self.obra.duracionExtendida

    def buscarDuracionResObra(self):
        return self.obra.druacionResumida

class Obra(models.Model):
    nombreOrba = models.CharField(u"Nombre", max_length=125)
    duracionExtendida = models.PositiveIntegerField(u"Duracion extendida", help_text="Medida en minutos")
    druacionResumida = models.PositiveIntegerField(u"Duracion resumida", help_text="Medida en minutos")
    
    def __str__(self):
        return self.nombreOrba