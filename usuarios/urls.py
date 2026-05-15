from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    # Sesión
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # CRUD Usuarios (solo admin/director)
    path('', views.lista_usuarios, name='lista_usuarios'),
    path('nuevo/', views.crear_usuario, name='crear_usuario'),
    path('<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),

    # Detalle de perfil
    path('<int:pk>/perfil/', views.detalle_usuario, name='detalle_usuario'),
]