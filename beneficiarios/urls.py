from django.urls import path
from . import views

app_name = 'beneficiarios'

urlpatterns = [
    # Beneficiarios - rutas fijas PRIMERO
    path('', views.lista_beneficiarios, name='lista_beneficiarios'),
    path('nuevo/', views.crear_beneficiario, name='crear_beneficiario'),

    # EXPORTACIONES BENEFICIARIOS
    path('exportar/excel/', views.exportar_excel_beneficiarios, name='exportar_excel_beneficiarios'),
    path('exportar/pdf/', views.exportar_pdf_beneficiarios, name='exportar_pdf_beneficiarios'),

    # ELIMINACIÓN MASIVA - antes de <str:ci>/
    path('eliminar-multiples/', views.eliminar_multiples_beneficiarios, name='eliminar_multiples_beneficiarios'),

    # Rutas con parámetro CI
    path('<str:ci>/', views.detalle_beneficiario, name='detalle_beneficiario'),
    path('<str:ci>/editar/', views.editar_beneficiario, name='editar_beneficiario'),
    path('<str:ci>/eliminar/', views.eliminar_beneficiario, name='eliminar_beneficiario'),

    # Tutores / padres - rutas fijas PRIMERO
    path('tutores/lista/', views.lista_tutores, name='lista_tutores'),
    path('tutores/nuevo/', views.crear_tutor, name='crear_tutor'),

    # EXPORTACIONES TUTORES
    path('tutores/exportar/excel/', views.exportar_excel_tutores, name='exportar_excel_tutores'),
    path('tutores/exportar/pdf/', views.exportar_pdf_tutores, name='exportar_pdf_tutores'),

    # ELIMINACIÓN MASIVA TUTORES - antes de tutores/<str:ci>/
    path('tutores/eliminar-multiples/', views.eliminar_multiples_tutores, name='eliminar_multiples_tutores'),

    # Rutas con CI de tutor
    path('tutores/<str:ci>/', views.detalle_tutor, name='detalle_tutor'),
    path('tutores/<str:ci>/editar/', views.editar_tutor, name='editar_tutor'),
    path('tutores/<str:ci>/eliminar/', views.eliminar_tutor, name='eliminar_tutor'),

    # Pre-inscripciones
    path('admin/preinscripciones/', views.lista_preinscripciones, name='lista_preinscripciones'),
    path('admin/preinscripciones/<int:pk>/', views.resolver_preinscripcion, name='resolver_preinscripcion'),
    path('admin/preinscripciones/<int:pk>/eliminar/', views.eliminar_preinscripcion, name='eliminar_preinscripcion'),
    path('admin/preinscripciones/<int:pk>/mover/', views.mover_preinscripcion, name='mover_preinscripcion'),
    path('admin/preinscripciones/<int:pk>/mover/beneficiario/', views.crear_beneficiario_desde_preinscripcion, name='crear_beneficiario_desde_preinscripcion'),
    path('admin/preinscripciones/<int:pk>/mover/tutor/', views.crear_tutor_desde_preinscripcion, name='crear_tutor_desde_preinscripcion'),
]