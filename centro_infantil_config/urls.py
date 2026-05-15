from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usuarios import views as uv
from beneficiarios import views as bv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', uv.dashboard, name='dashboard'),
    path('dashboard/', uv.dashboard, name='dashboard'),
    path('usuarios/', include('usuarios.urls')),
    path('beneficiarios/', include('beneficiarios.urls')),
    path('ninos/', include('ninos.urls')),
    path('grupos/', include('grupos.urls')),
    path('asistencia/', include('asistencia.urls', namespace='asistencia')),
    path('inventario/', include('inventario.urls', namespace='inventario')),
    path('evaluaciones/', include('evaluaciones.urls', namespace='evaluaciones')),
    # Rutas públicas
    path('pre-inscripcion/', bv.preinscripcion_publica, name='preinscripcion_publica'),
    path('pre-inscripcion/enviada/', bv.preinscripcion_confirmacion, name='preinscripcion_confirmacion'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
