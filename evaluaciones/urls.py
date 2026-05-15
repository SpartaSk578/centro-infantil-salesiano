from django.urls import path
from . import views

# Esta línea permite el uso del namespace 'evaluaciones:' en tus plantillas
app_name = 'evaluaciones'

urlpatterns = [
    # Ruta principal: Lista de evaluaciones
    path('', views.lista_evaluaciones, name='lista_evaluaciones'),
    
    # Ruta para crear una nueva evaluación
    path('nueva/', views.crear_evaluacion, name='crear_evaluacion'),
    
    # Ruta para editar una evaluación existente mediante su ID (pk)
    path('<int:pk>/editar/', views.editar_evaluacion, name='editar_evaluacion'),
    
    # Ruta para eliminar una evaluación mediante su ID (pk)
    path('<int:pk>/eliminar/', views.eliminar_evaluacion, name='eliminar_evaluacion'),
]