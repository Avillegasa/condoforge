from django.urls import path
from .views import login_view, logout_view, user_list, user_create, user_edit, user_delete, user_profile, password_change
from .views import  listado_copropietarios, exportar_copropietarios_excel, exportar_copropietarios_pdf, editar_copropietario, cambiar_contrasena, eliminar_copropietario

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('list/', user_list, name='user_list'),
    path('create/', user_create, name='user_create'),
    path('edit/<int:pk>/', user_edit, name='user_edit'),
    path('delete/<int:pk>/', user_delete, name='user_delete'),
    path('password_change/', password_change, name='password_change'),
    path('profile/<int:pk>/', user_profile, name='user_profile'),

    path("copropietarios/", listado_copropietarios, name="listado_copropietarios"),
    path("copropietarios/exportar-excel/", exportar_copropietarios_excel, name="exportar_copropietarios_excel"),
    path("copropietarios/exportar-pdf/", exportar_copropietarios_pdf, name="exportar_copropietarios_pdf"),
    path("copropietarios/editar/<int:user_id>/", editar_copropietario, name="editar_copropietario"),
    path("copropietarios/cambiar-contrasena/<int:user_id>/", cambiar_contrasena, name="cambiar_contrasena"),
    path("copropietarios/eliminar/<int:user_id>/", eliminar_copropietario, name="eliminar_copropietario"),
]
