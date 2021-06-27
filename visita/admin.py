from django.contrib import admin
from .models import Escuela, TipoVista, Estado, CambioEstado, ReservaVisita, AsigacionVisita

admin.site.register(Escuela)
admin.site.register(TipoVisita)
admin.site.register(Estado)
admin.site.register(CambioEstado)
admin.site.register(ReservaVisita)
admin.site.register(AsignacionVisita)
