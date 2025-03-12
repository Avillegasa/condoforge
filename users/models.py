from django.contrib.auth.models import AbstractUser
from django.db import models
from vivienda.models import Vivienda

class CustomUser(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('portero', 'Portero'),
        ('limpieza', 'Personal de limpieza'),
        ('visitante', 'Visitante'),
    ]

    HABITANTE_TYPES = [
        ('titular', 'Titular'),
        ('dueno', 'Dueño'),
        ('copropietario', 'Copropietario'),
        ('menor', 'Menor'),
    ]

    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLES, default='visitante')
    tipo_habitante = models.CharField(max_length=20, choices=HABITANTE_TYPES, blank=True, null=True)
    vivienda = models.ForeignKey(
        'vivienda.Vivienda',  # Especificamos el modelo correctamente
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="residentes"  # Cambiamos el related_name para evitar conflicto
    )   
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.get_tipo_habitante_display()}"
