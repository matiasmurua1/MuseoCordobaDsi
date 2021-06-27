from django.contrib import admin
from .models import Sede, PublicoDestino, TipoExposicion, Exposicion, Obra
# Register your models here.

admin.site.register(Sede)
admin.site.register(PublicoDestino)
admin.site.register(TipoExposicion)
admin.site.register(Exposicion)
admin.site.register(Obra)
