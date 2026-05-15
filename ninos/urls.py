from django.urls import path
from . import views

app_name = 'ninos'

urlpatterns = [
    path('', views.lista_ninos, name='lista_ninos'),
    path('nuevo/', views.crear_nino, name='crear_nino'),
    path('<int:pk>/', views.detalle_nino, name='detalle_nino'),
    path('<int:pk>/editar/', views.editar_nino, name='editar_nino'),
    path('<int:pk>/eliminar/', views.eliminar_nino, name='eliminar_nino'),
    path('<int:pk>/documento/subir/', views.subir_documento, name='subir_documento'),
    path('documento/<int:pk>/eliminar/', views.eliminar_documento, name='eliminar_documento'),
    path('exportar/excel/', views.exportar_excel_ninos, name='exportar_excel_ninos'),
    path('exportar/pdf/', views.exportar_pdf_ninos, name='exportar_pdf_ninos'),
    path('importar/', views.importar_excel_ninos, name='importar_excel_ninos'),
    path('eliminar-multiples/', views.eliminar_multiples_ninos, name='eliminar_multiples_ninos'),
]
