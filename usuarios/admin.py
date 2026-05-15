from django.contrib import admin
from .models import Usuario, Rol

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_rol')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # Usamos ModelAdmin básico, NO el de usuarios de Django, para evitar el error de la imagen
    list_display = ('nombre_usuario', 'email', 'id_rol', 'is_staff')
    search_fields = ('nombre_usuario', 'email')
    
    # Esta lista de campos es simple y directa
    fields = (
        'nombre_usuario', 
        'password', 
        'email', 
        'nombres', 
        'apellidos', 
        'id_rol', 
        'estado', 
        'is_staff', 
        'is_active', 
        'is_superuser'
    )