from django.db import models
from django.conf import settings

class Alarma(models.Model):
    TIPO_CHOICES = [
        ('accidente', 'Accidente'),
        ('extravio_mascota', 'Extravío de Mascota'),
        ('otro', 'Otro Evento')
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"