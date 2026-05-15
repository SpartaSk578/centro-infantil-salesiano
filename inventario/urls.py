from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.lista_inventario, name='lista_inventario'),
    path('nuevo/', views.crear_item, name='crear_item'),
    path('<int:pk>/editar/', views.editar_item, name='editar_item'),
    path('<int:pk>/eliminar/', views.eliminar_item, name='eliminar_item'),
]
