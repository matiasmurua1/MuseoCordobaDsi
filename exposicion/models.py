from django.db import models

# Create your models here.
class Sede(models.Model):
    cantMaximaVisita = models.PositiveIntegerField(u"Cantidad maxima de visitantes")
    cantMaximaPorGuia = models.PositiveIntegerField(u"Cantidad maxima por guia")
    """ El atributo es de tipo int que solo acepta valores positivos"""
    nombre = models.CharField(u"Nombre", max_length=64)

    def buscarDuracionExposiciones(self):
        pass

    def buscarExposiciones(self):
        pass

    def buscarResParaFechaHora(self):
        pass

class PublicoDestino(models.Model):
    nombre = models.CharField(u"Nombre", max_length=64)

class TipoExposicion(models.Model):
    TEMPORAL = "Tem"
    NOMBRE_CHOICES = [
        (TEMPORAL, "Temporal"),
    ]

    nombre = models.CharField(u"Nombre", choices=NOMBRE_CHOICES, max_length=3)

    def esTemporal(self):
        pass

class Exposicion(models.Model):
    fechaFin = models.DateField(u"Fecha fin")
    fechaInicio = models.DateField(u"Fecha inicio")
    fechaFinReplanificada = models.DateField(u"Fecha fin replanificada", null=True)
    """Parametro null=True para permitir guardar un atributo con valor nulo"""
    fechaInicioReplanificada = models.DateField(u"Fecha inicio replanificada", null=True)
    horaApertura = models.TimeField(u"Hora apertura")
    horaCierre = models.TimeField(u"Hora cierre")
    nombre = models.CharField(u"Nombre", max_length=64)
    publicoDestino = models.ManyToManyField("PublicoDestino")
    tipoExposicion = models.ForeignKey("TipoExposicion", on_delete=models.PROTECT)
    sede = models.ForeignKey("Sede", on_delete=models.PROTECT, related_name="exposicion")

    def buscarDuracionExtObra(self):
        pass

    def getHorarioHabilitado(self):
        pass

    def getTempVigentes(self):
        pass

class DetalleExposicion(models.Model):
    obra = models.ForeignKey("Obra", on_delete=models.PROTECT)
    exposicion = models.ForeignKey("Exposicion", on_delete=models.PROTECT, related_name="detalleExposicion")

    def buscarDuracionExtObra(self):
        pass

class Obra(models.Model):
    duracionExtendida = models.PositiveIntegerField(u"Duracion extendida", help_text="Duracion en minutos")
