from django.contrib import admin
from .models import Alarma

@admin.register(Alarma)
class AlarmaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'descripcion', 'fecha_creacion')
    list_filter = ('tipo', 'fecha_creacion')