from django.utils.timezone import timedelta
from django.utils import timezone

from visita.models import (
        Escuela, TipoVisita, 
        ReservaVisita, Estado
    )
from exposicion.models import Sede
from empleado.models import Empleado

class GestorRegReservaVisitaGuiada():
    def __init__(self):
        self._tipoVisita = None
        self._duracionEstimadaVisita = None
        self._cantidadVisitantes = None
        self._fechaHoraReserva = None
        self._fechaHoraReservaFin = None
        self._guias = []
        self._exposiciones = []
        self._sedeSeleccionada = None
        self._escuela = None
        self._fechaHoraActual = None
        self._empleadoLogueado = None
        self._estadoReserva = None
        self._numeroUnicoReserva = None

    @property
    def estadoReserva(self):
        return self._estadoReserva
    
    @estadoReserva.setter
    def estadoReserva(self, estado):
        self._estadoReserva = estado

    @property
    def empleadoLogueado(self):
        return self._empleadoLogueado
    
    @empleadoLogueado.setter
    def empleadoLogueado(self, empleado):
        self._empleadoLogueado = empleado

    @property
    def escuela(self):
        return self._escuela
    
    @escuela.setter
    def escuela(self, objetoEscuela):
        self._escuela = objetoEscuela
    
    @property
    def cantidadVisitantes(self):
        return self._cantidadVisitantes

    @cantidadVisitantes.setter
    def cantidadVisitantes(self, cantidad):
        self._cantidadVisitantes = cantidad
    
    @property
    def sedeSeleccionada(self):
        return self._sedeSeleccionada
    
    @sedeSeleccionada.setter
    def sedeSeleccionada(self, sede):
        self._sedeSeleccionada = sede
    
    @property
    def tipoVisita(self):
        return self._tipoVisita
    
    @tipoVisita.setter
    def tipoVisita(self, tipoVisita):
        self._tipoVisita = tipoVisita

    @property
    def fechaHoraReserva(self):
        return self._fechaHoraReserva

    @fechaHoraReserva.setter
    def fechaHoraReserva(self, fechaHoraInicio):
        self._fechaHoraReserva = fechaHoraInicio

    @property
    def fechaHoraReservaFin(self):
        return self._fechaHoraReservaFin
    
    @fechaHoraReservaFin.setter
    def fechaHoraReservaFin(self, fechaHoraFin):
        self._fechaHoraReservaFin = fechaHoraFin
    
    @property
    def fechaHoraActual(self):
        return self._fechaHoraActual
    
    @fechaHoraActual.setter
    def fechaHoraActual(self, fechaHora):
        self._fechaHoraActual = fechaHora

    @property
    def exposiciones(self):
        return self._exposiciones
    
    # Patron experto
    @exposiciones.setter
    def exposiciones(self, exposicionesSeleccionadas):
        exposiciones_qs = self._sedeSeleccionada.exposicion.filter(
            pk__in=exposicionesSeleccionadas)
        self._exposiciones = exposiciones_qs
    
    @property
    def guias(self):
        return self._guias
    
    @guias.setter
    def guias(self, guiasSeleccionados):
        guias_qs = Empleado.objects.filter(pk__in=guiasSeleccionados)
        self._guias = guias_qs

    @property
    def numeroUnicoReserva(self):
        return self._numeroUnicoReserva
    
    @numeroUnicoReserva.setter
    def numeroUnicoReserva(self, numero):
        self._numeroUnicoReserva = numero

    def buscarEscuelas(self):
        allEscuelas = []
        for escuela in Escuela.objects.all():
            allEscuelas.append(escuela.nombre)
        return allEscuelas
    
    def buscarSedes(self):
        sedes = []
        for sede in Sede.objects.all():
            sedes.append(sede.nombre)
        return sedes

    def buscarTipoVisita(self):
        tiposVisita = []
        opciones = [TipoVisita.COMPLETA, TipoVisita.POR_EXPOSICION]
        for tipoVisita in TipoVisita.objects.filter(nombre__in=opciones):
            id_tipoVisita, nombre_tipoVisita = tipoVisita.get_nombre()
            tiposVisita.append({
                'id': id_tipoVisita, 
                'nombre':nombre_tipoVisita
            })
        return tiposVisita
    
    def tomarFechaHoraActual(self):
        return timezone.now()

    def buscarExposicionesTempVigentes(self):
        self._fechaHoraActual = self.tomarFechaHoraActual()
        exposicionesTempVigentes = \
            self.sedeSeleccionada.buscarExposiciones(
                    self._fechaHoraActual.date(),
                    self._tipoVisita.esCompleta()
                )
        return {
            'esPorExposicion': self._tipoVisita.esPorExposicion(), 
            'esCompleta': self._tipoVisita.esCompleta(), 
            'exposiciones': exposicionesTempVigentes
        }
    
    def calcularDuracionExposiciones(self):
        self._duracionEstimadaVisita = self._sedeSeleccionada.buscarDuracionExposiciones(
            self._exposiciones, 
            completa=(self._tipoVisita.esCompleta()), 
            porExposicion=(self._tipoVisita.esPorExposicion()))
        return self._duracionEstimadaVisita
    
    def calcularCapMaxSobrepasada(self):
        visitantesEnMuseo = self._sedeSeleccionada.buscarResParaFechaHora(
            self._fechaHoraReserva, 
            self._fechaHoraReservaFin)
        cantidadMaxima = self._sedeSeleccionada.cantMaximaVisita
        return visitantesEnMuseo + self._cantidadVisitantes > cantidadMaxima

    def calcularCantMaxGuiasNecesarios(self):
        guiasNecesarios = self._cantidadVisitantes // self._sedeSeleccionada.cantMaximaPorGuia
        if (self._cantidadVisitantes % self._sedeSeleccionada.cantMaximaPorGuia > 0):
            return guiasNecesarios + 1
        return guiasNecesarios

    def buscarGuiasDispFechaReserva(self):
        guias = []
        for empleado in Empleado.objects.filter(sede=self._sedeSeleccionada):
            guia = empleado.getGuiaDispEnHorario(
                self._fechaHoraReserva,
                self._fechaHoraReservaFin
            )
            if guia is not None:
                guias.append(guia)
        return guias
    
    def buscarEstadoReserva(self):
        for estado in Estado.objects.all():
            if estado.esAmbitoReserva() and estado.esPendienteDeConfirmacion():
                self._estadoReserva = estado
                return estado
        return None 
    
    def buscarUltimoNumReserva(self):
        self.numeroUnicoReserva = ReservaVisita.objects.getNumeroReserva() + 1

    def crearReserva(self):
        ReservaVisita.objects.new(
            self._cantidadVisitantes,
            self._duracionEstimadaVisita,
            self._fechaHoraReserva,
            self._numeroUnicoReserva,
            self._exposiciones,
            self._sedeSeleccionada,
            self._estadoReserva,
            self._guias,
            self._fechaHoraReservaFin,
            self._fechaHoraActual,
            self._escuela
        )