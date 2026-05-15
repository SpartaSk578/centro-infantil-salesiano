from django.urls import path
from . import views

# Esta línea soluciona el error "'grupos' is not a registered namespace"
app_name = 'grupos' 

urlpatterns = [
    # Esta es la ruta que busca el menú: {% url 'grupos:lista_grupos' %}
    path('', views.lista_grupos, name='lista_grupos'),
    
    path('nuevo/', views.crear_grupo, name='crear_grupo'),
    path('<int:pk>/', views.detalle_grupo, name='detalle_grupo'),
    path('<int:pk>/editar/', views.editar_grupo, name='editar_grupo'),
    path('<int:pk>/eliminar/', views.eliminar_grupo, name='eliminar_grupo'),
]