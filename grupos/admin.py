from django.contrib import admin
from .models import Grupo
@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ['nombre_grupo', 'educador_responsable']
