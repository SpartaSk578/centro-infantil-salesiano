from django.urls import path
from . import views

app_name = 'asistencia'

urlpatterns = [
    path('', views.lista_asistencia, name='lista_asistencia'),
    path('pasar-lista/', views.registrar_asistencia_masiva, name='asistencia_masiva'),
    path('individual/<int:nino_id>/', views.registrar_asistencia_individual, name='asistencia_individual'),
]
