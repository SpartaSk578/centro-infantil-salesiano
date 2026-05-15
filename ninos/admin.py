from django.contrib import admin
from .models import Nino, DocumentoNino

class DocumentoInline(admin.TabularInline):
    model = DocumentoNino
    extra = 1

@admin.register(Nino)
class NinoAdmin(admin.ModelAdmin):
    inlines = [DocumentoInline]
    list_display = ['get_full_name', 'sexo', 'id_grupo', 'fecha_nacimiento']
    search_fields = ['nombres', 'apellido_paterno', 'apellido_materno']

admin.site.register(DocumentoNino)
