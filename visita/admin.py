from django.contrib import admin
from .models import Escuela, TipoVisita, Estado, CambioEstado, ReservaVisita, AsignacionVisita


admin.site.register(Escuela)
admin.site.register(TipoVisita)
admin.site.register(Estado)
admin.site.register(CambioEstado)
admin.site.register(ReservaVisita)
admin.site.register(AsignacionVisita)
