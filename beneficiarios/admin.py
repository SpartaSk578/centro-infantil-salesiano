from django.contrib import admin
# IMPORTANTE: No importamos 'Rol' aquí, porque Rol pertenece a la app 'usuarios'
from .models import Beneficiario, TutorPadre, PreInscripcion

@admin.register(Beneficiario)
class BeneficiarioAdmin(admin.ModelAdmin):
    # 'contacto' es el campo que agregamos para el celular del beneficiario
    list_display = ('CI_beneficiario', 'nombres', 'apellido_paterno', 'contacto')
    search_fields = ('CI_beneficiario', 'nombres', 'apellido_paterno')
    list_filter = ('apellido_paterno',)

@admin.register(TutorPadre)
class TutorPadreAdmin(admin.ModelAdmin):
    # 'contacto' aquí es el celular del tutor que necesitabas para el reporte
    list_display = ('CI_tutor', 'nombres', 'apellido_paterno', 'contacto')
    search_fields = ('CI_tutor', 'nombres', 'apellido_paterno')

@admin.register(PreInscripcion)
class PreInscripcionAdmin(admin.ModelAdmin):
    list_display = ('nombres_nino', 'nombres_tutor', 'telefono', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombres_nino', 'nombres_tutor')