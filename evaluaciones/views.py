from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Evaluacion
from .forms import EvaluacionForm
from ninos.models import Nino
from grupos.models import Grupo

def _get_rol(user):
    return user.id_rol.nombre_rol if user.id_rol else ''

@login_required
def lista_evaluaciones(request):
    q = request.GET.get('q', '')
    periodo = request.GET.get('periodo', '')
    evaluaciones = Evaluacion.objects.select_related('id_nino', 'registrado_por').order_by('-fecha')

    # Educadora solo ve su grupo
    rol = _get_rol(request.user)
    if rol == 'Educadora':
        grupo = Grupo.objects.filter(educador_responsable=request.user).first()
        if grupo:
            evaluaciones = evaluaciones.filter(id_nino__id_grupo=grupo)
        else:
            evaluaciones = evaluaciones.none()

    if q:
        evaluaciones = evaluaciones.filter(
            Q(id_nino__nombres__icontains=q) | Q(id_nino__apellidos__icontains=q)
        )
    if periodo:
        evaluaciones = evaluaciones.filter(periodo__icontains=periodo)

    periodos = Evaluacion.objects.values_list('periodo', flat=True).distinct()
    return render(request, 'evaluaciones/lista.html', {
        'evaluaciones': evaluaciones, 'q': q, 'periodo': periodo, 'periodos': periodos
    })

@login_required
def crear_evaluacion(request):
    rol = _get_rol(request.user)
    form = EvaluacionForm(request.POST or None)

    # Filtrar niños del grupo si es educadora
    if rol == 'Educadora':
        grupo = Grupo.objects.filter(educador_responsable=request.user).first()
        if grupo and 'id_nino' in form.fields:
            form.fields['id_nino'].queryset = Nino.objects.filter(id_grupo=grupo)

    if request.method == 'POST' and form.is_valid():
        e = form.save(commit=False)
        e.registrado_por = request.user
        e.save()
        messages.success(request, 'Evaluación registrada correctamente.')
        return redirect('evaluaciones:lista_evaluaciones')
    return render(request, 'evaluaciones/form.html', {'form': form, 'titulo': 'Nueva Evaluación'})

@login_required
def editar_evaluacion(request, pk):
    e = get_object_or_404(Evaluacion, pk=pk)
    form = EvaluacionForm(request.POST or None, instance=e)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Evaluación actualizada.')
        return redirect('evaluaciones:lista_evaluaciones')
    return render(request, 'evaluaciones/form.html', {'form': form, 'titulo': 'Editar Evaluación', 'objeto': e})

@login_required
def eliminar_evaluacion(request, pk):
    e = get_object_or_404(Evaluacion, pk=pk)
    if request.method == 'POST':
        e.delete()
        messages.success(request, 'Evaluación eliminada.')
        return redirect('evaluaciones:lista_evaluaciones')
    return render(request, 'confirmar_eliminar.html', {'objeto': e, 'tipo': 'evaluación'})

from django.db.models import Q
