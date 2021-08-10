from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from django.utils.timezone import timedelta, datetime, make_aware
from django.utils import timezone

from exposicion.models import Sede
from empleado.models import Empleado
from .models import Escuela, TipoVisita
from .vendor.GestorRegReservaVisitaGuiada import GestorRegReservaVisitaGuiada

gestor = GestorRegReservaVisitaGuiada()

# Create your views here.
@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")

@login_required(login_url="/login/")
def registrarReservaVisitaGuiada(request):
    return render(request, "PantallaRegReservaVisitaGuiada.html")

# Le dice al gestor que busque las escuelas y devuelve el listado de nombres
def tomarRegReservaVisitaGuiada(request):
    return JsonResponse({"escuelas": gestor.buscarEscuelas()})

def tomarSeleccionEscuela(request):
    data = request.POST
    gestor.escuela = Escuela.objects.get(nombre=data["escuela"])
    return HttpResponse()

# Guarda la cantidad ingresada en el gestor y busca las sedes
def tomarCantVisitantes(request):
    gestor.cantidadVisitantes = int(request.POST["cantidadVisitantes"])
    return JsonResponse({'sedes': gestor.buscarSedes()})

def tomarSeleccionSede(request):
    sedeSeleccionada = Sede.objects.get(nombre=request.POST["sede"])
    gestor.sedeSeleccionada = sedeSeleccionada
    return JsonResponse({'tiposVisita': gestor.buscarTipoVisita()})

def tomarSeleccionTipoVisita(request):
    data = request.POST
    tipoVisita = TipoVisita.objects.get(nombre=data['tipoVisita'])
    gestor.tipoVisita = tipoVisita
    
    responseData = gestor.buscarExposicionesTempVigentes()
    return JsonResponse(responseData)

def tomarFechaHoraReserva(request):
    data = request.POST
    # Toma la fecha y la hora ingresada por el usuario lo transforma en un objeto de tipo DateTime
    # Luego lo transforma de un DateTime sin zona horaria a un objeto con zona horaria
    # Dado que la base de datos esta configurada para funcionar teniendo en cuenta las zonas horarias
    fechaHoraReserva = make_aware(parse_datetime(f'{data["fechaReserva"]} {data["horaReserva"]}'))
    gestor.fechaHoraReserva = fechaHoraReserva
    gestor.exposiciones = data.getlist("exposicionesSeleccionadas[]") 
    
    duracionExposiciones = gestor.calcularDuracionExposiciones()

    # Arma objeto datetime para la finalizacion de la reserva en base a la hora inicial de la reserva 
    # y los minutos estimados que dura la visita
    gestor.fechaHoraReservaFin = fechaHoraReserva + timedelta(minutes=duracionExposiciones)
    
    max_overflow = gestor.calcularCapMaxSobrepasada()
        
    if max_overflow is True:
        return JsonResponse(
            {"msg": "Capacidad maxima de visitantes alcanzada"}, 
            status=403)
        
    guiasNecesarios = gestor.calcularCantMaxGuiasNecesarios()

    guiasDisponibles = gestor.buscarGuiasDispFechaReserva()
    
    return JsonResponse({
        "guias":guiasDisponibles, 
        "necesarios":guiasNecesarios,
        "duracion": duracionExposiciones
        })

def tomarGuias(request):
    data = request.POST
    gestor.guias = data.getlist("guias[]")
    return HttpResponse(200)

def registrarVisita(request):
    data = request.POST
    gestor.empleadoLogueado = buscarEmpleadoLogueado(request)
    
    # Patron experto
    gestor.buscarUltimoNumReserva()
    
    estadoInicial = gestor.buscarEstadoReserva()
    
    if estadoInicial is None:
        return JsonResponse({"msg":"No existe el estado incial"}, status=404)

    # Patron Creador
    # Le deja la responsabilidad al ReservaVisitaManager
    gestor.crearReserva()
    return HttpResponse(201)

def buscarEmpleadoLogueado(request):
    # Obtiene el usuario logueado desde la sesion (objeto proveniente de
    # del request provisto por Django) y luego obtiene el objeto empleado
    # desde el usuario
    return request.user.empleado