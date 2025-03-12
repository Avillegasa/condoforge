from django.urls import path
from .views import lista_viviendas, detalle_vivienda, editar_vivienda, agregar_integrante, registrar_mascota, crear_vivienda, detalle_mascota

urlpatterns = [
    path("", lista_viviendas, name="lista_viviendas"),
    path("<int:vivienda_id>/", detalle_vivienda, name="detalle_vivienda"),
    path("<int:vivienda_id>/editar/", editar_vivienda, name="editar_vivienda"),
    path("<int:vivienda_id>/agregar-integrante/", agregar_integrante, name="agregar_integrante"),
    path("<int:vivienda_id>/registrar-mascota/", registrar_mascota, name="registrar_mascota"),
    path("crear/", crear_vivienda, name="crear_vivienda"),
    path("mascota/<int:mascota_id>/", detalle_mascota, name="detalle_mascota"),
]
