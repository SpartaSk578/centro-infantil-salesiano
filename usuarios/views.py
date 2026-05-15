from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Usuario, Rol
from .forms import LoginForm, UsuarioForm


# ─── HELPERS DE ROL ──────────────────────────────────────────────────────────
def _get_rol(user):
    if not user.is_authenticated or not user.id_rol:
        return ''
    return user.id_rol.nombre_rol.lower()

def _es_admin_director(user):
    return _get_rol(user) in ['administrador', 'director', 'directora']

def _es_educadora(user):
    return _get_rol(user) in ['educadora', 'educador']


# ─── SESIÓN ──────────────────────────────────────────────────────────────────
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        user.ultimo_acceso = timezone.now()
        user.save(update_fields=['ultimo_acceso'])
        login(request, user)
        return redirect('dashboard')
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('usuarios:login')


# ─── DASHBOARD ───────────────────────────────────────────────────────────────
@login_required
def dashboard(request):
    from ninos.models import Nino
    from beneficiarios.models import Beneficiario, PreInscripcion
    from asistencia.models import Asistencia
    from evaluaciones.models import Evaluacion
    from grupos.models import Grupo
    from datetime import date
    hoy = date.today()
    ctx = {
        'total_ninos': Nino.objects.count(),
        'total_beneficiarios': Beneficiario.objects.count(),
        'total_grupos': Grupo.objects.count(),
        'total_usuarios': Usuario.objects.count(),
        'asistencia_hoy': Asistencia.objects.filter(fecha=hoy).count(),
        'presentes_hoy': Asistencia.objects.filter(fecha=hoy, estado='asistio').count(),
        'ausentes_hoy': Asistencia.objects.filter(fecha=hoy, estado='falto').count(),
        'ultimas_evaluaciones': Evaluacion.objects.select_related('id_nino').order_by('-fecha')[:5],
        'hoy': hoy,
        'preinscripciones_pendientes': PreInscripcion.objects.filter(estado='pendiente').count(),
        'gestion': hoy.year,
        'es_admin_director': _es_admin_director(request.user),
        'es_educadora': _es_educadora(request.user),
    }
    return render(request, 'dashboard.html', ctx)


# ─── USUARIOS ────────────────────────────────────────────────────────────────
@login_required
def lista_usuarios(request):
    # Educadoras solo ven la lista pero no pueden crear/editar/eliminar
    usuarios = Usuario.objects.select_related('id_rol').all()
    return render(request, 'usuarios/lista.html', {
        'usuarios': usuarios,
        'puede_gestionar': _es_admin_director(request.user),
    })

@login_required
def detalle_usuario(request, pk):
    # Solo admin/director ven el detalle completo
    if not _es_admin_director(request.user):
        messages.error(request, 'No tienes permiso para ver el perfil de otros usuarios.')
        return redirect('usuarios:lista_usuarios')
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'usuarios/detalle.html', {'usuario': usuario})

@login_required
def crear_usuario(request):
    if not _es_admin_director(request.user):
        messages.error(request, 'No tienes permiso para crear usuarios.')
        return redirect('usuarios:lista_usuarios')
    form = UsuarioForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        if request.FILES.get('foto_perfil'):
            user.foto_perfil = request.FILES['foto_perfil']
        user.save()
        messages.success(request, 'Usuario creado correctamente.')
        return redirect('usuarios:lista_usuarios')
    return render(request, 'usuarios/form.html', {'form': form, 'titulo': 'Nuevo Usuario'})

@login_required
def editar_usuario(request, pk):
    if not _es_admin_director(request.user):
        messages.error(request, 'No tienes permiso para editar usuarios.')
        return redirect('usuarios:lista_usuarios')
    usuario = get_object_or_404(Usuario, pk=pk)
    form = UsuarioForm(request.POST or None, request.FILES or None, instance=usuario)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        if request.FILES.get('foto_perfil'):
            user.foto_perfil = request.FILES['foto_perfil']
        user.save()
        messages.success(request, 'Usuario actualizado.')
        return redirect('usuarios:lista_usuarios')
    return render(request, 'usuarios/form.html', {
        'form': form, 'titulo': 'Editar Usuario', 'objeto': usuario
    })

@login_required
def eliminar_usuario(request, pk):
    if not _es_admin_director(request.user):
        messages.error(request, 'No tienes permiso para eliminar usuarios.')
        return redirect('usuarios:lista_usuarios')
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado.')
        return redirect('usuarios:lista_usuarios')
    return render(request, 'confirmar_eliminar.html', {'objeto': usuario, 'tipo': 'usuario'})