from django.contrib import admin
from .models import Sede, HorarioSede, PublicoDestino, TipoExposicion, Exposicion, Obra, DetalleExposicion
# Register your models here.

admin.site.register(Sede)
admin.site.register(PublicoDestino)
admin.site.register(TipoExposicion)
admin.site.register(Exposicion)
admin.site.register(Obra)
admin.site.register(DetalleExposicion)
admin.site.register(HorarioSede)
