from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Asistencia
from .forms import AsistenciaForm, AsistenciaMasivaForm
from ninos.models import Nino
from grupos.models import Grupo
from datetime import date

def _get_rol(user):
    return user.id_rol.nombre_rol if user.id_rol else ''

def _get_grupo_educadora(user):
    if _get_rol(user) == 'Educadora':
        return Grupo.objects.filter(educador_responsable=user).first()
    return None

@login_required
def lista_asistencia(request):
    fecha = request.GET.get('fecha', str(date.today()))
    grupo_id = request.GET.get('grupo', '')

    ninos_queryset = Nino.objects.select_related('id_grupo')

    # Educadora solo ve su grupo
    grupo_educadora = _get_grupo_educadora(request.user)
    if grupo_educadora:
        ninos_queryset = ninos_queryset.filter(id_grupo=grupo_educadora)
        grupos = [grupo_educadora]
    else:
        if grupo_id:
            ninos_queryset = ninos_queryset.filter(id_grupo_id=grupo_id)
        grupos = Grupo.objects.all()

    asistencias = Asistencia.objects.filter(fecha=fecha).select_related('id_nino', 'registrado_por')
    asistencia_map = {a.id_nino_id: a for a in asistencias}

    for nino in ninos_queryset:
        nino.asistencia_info = asistencia_map.get(nino.id)

    return render(request, 'asistencia/lista.html', {
        'ninos': ninos_queryset,
        'asistencia_map': asistencia_map,
        'fecha': fecha,
        'grupos': grupos,
        'grupo_id': grupo_id,
        'grupo_educadora': grupo_educadora,
        'presentes': asistencias.filter(estado='asistio').count(),
        'ausentes': asistencias.filter(estado='falto').count(),
        'permisos': asistencias.filter(estado='permiso').count(),
    })

@login_required
def registrar_asistencia_masiva(request):
    fecha = request.POST.get('fecha') or request.GET.get('fecha') or str(date.today())
    grupo_id = request.POST.get('grupo_id') or request.GET.get('grupo_id') or ''

    grupo_educadora = _get_grupo_educadora(request.user)

    ninos = Nino.objects.select_related('id_grupo').all()
    if grupo_educadora:
        ninos = ninos.filter(id_grupo=grupo_educadora)
    elif grupo_id:
        ninos = ninos.filter(id_grupo_id=grupo_id)

    if request.method == 'POST' and 'guardar' in request.POST:
        for nino in ninos:
            estado = request.POST.get(f'estado_{nino.id}', 'falto')
            obs = request.POST.get(f'obs_{nino.id}', '')
            tipo_permiso = request.POST.get(f'permiso_{nino.id}', '') if estado == 'permiso' else ''

            Asistencia.objects.update_or_create(
                fecha=fecha,
                id_nino=nino,
                defaults={
                    'estado': estado,
                    'tipo_permiso': tipo_permiso or None,
                    'observaciones': obs,
                    'registrado_por': request.user,
                }
            )
        messages.success(request, f'Asistencia del {fecha} guardada correctamente.')
        return redirect('asistencia:lista_asistencia')

    asistencias_existentes = {
        a.id_nino_id: a
        for a in Asistencia.objects.filter(fecha=fecha, id_nino__in=ninos)
    }
    for nino in ninos:
        nino.asistencia_actual = asistencias_existentes.get(nino.id)

    grupos = Grupo.objects.all()
    return render(request, 'asistencia/masiva.html', {
        'ninos': ninos,
        'fecha': fecha,
        'grupos': grupos,
        'grupo_id': grupo_id,
        'grupo_educadora': grupo_educadora,
        'estados': Asistencia.ESTADO_CHOICES,
        'tipos_permiso': Asistencia.TIPO_PERMISO_CHOICES,
    })

@login_required
def registrar_asistencia_individual(request, nino_id):
    nino = get_object_or_404(Nino, pk=nino_id)
    fecha = request.POST.get('fecha', str(date.today()))
    estado = request.POST.get('estado', 'asistio')
    tipo_permiso = request.POST.get('tipo_permiso', '') if estado == 'permiso' else ''
    obs = request.POST.get('observaciones', '')

    Asistencia.objects.update_or_create(
        fecha=fecha,
        id_nino=nino,
        defaults={
            'estado': estado,
            'tipo_permiso': tipo_permiso or None,
            'observaciones': obs,
            'registrado_por': request.user,
        }
    )
    messages.success(request, f'Asistencia de {nino.get_full_name()} registrada.')
    return redirect(request.META.get('HTTP_REFERER', 'asistencia:lista_asistencia'))
