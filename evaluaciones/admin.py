from django.contrib import admin
from .models import Evaluacion
@admin.register(Evaluacion)
class EvaluacionAdmin(admin.ModelAdmin):
    list_display = ['id_nino', 'fecha', 'periodo', 'clasificacion', 'registrado_por']
    list_filter = ['clasificacion', 'periodo']
