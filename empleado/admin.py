from django.contrib import admin
from .models import Empleado, HorarioEmpleado, DiaSemana, Cargo


admin.site.register(Cargo)
admin.site.register(DiaSemana)
admin.site.register(Empleado)
admin.site.register(HorarioEmpleado)
