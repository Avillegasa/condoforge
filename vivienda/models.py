from django.db import models
from django.conf import settings

class Vivienda(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    titular = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="titular_vivienda")
    habitantes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="habitantes_vivienda", blank=True)
    mascotas = models.ManyToManyField("Mascota", blank=True, related_name="viviendas_asociadas")

    def numero_habitantes(self):
        return self.habitantes.count()

    def numero_mascotas(self):
        return self.mascotas.count()

    def __str__(self):
        return f"Vivienda {self.codigo}"
    
class Mascota(models.Model):
    vivienda = models.ForeignKey(Vivienda, on_delete=models.CASCADE, related_name="mascotas_vivienda")
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=30, choices=[("Perro", "Perro"), ("Gato", "Gato"), ("Otro", "Otro")])
    raza = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to="mascotas/", blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"