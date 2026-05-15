from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Grupo
from .forms import GrupoForm

ROL_EDUCADORA = 'Educadora'

@login_required
def lista_grupos(request):
    rol = request.user.id_rol.nombre_rol if request.user.id_rol else ''

    # Si es educadora, redirigir directo a su sala
    if rol == ROL_EDUCADORA:
        grupo = Grupo.objects.filter(educador_responsable=request.user).first()
        if grupo:
            return redirect('grupos:detalle_grupo', pk=grupo.pk)
        else:
            messages.warning(request, 'No tienes ninguna sala asignada aún.')
            return render(request, 'grupos/lista.html', {'grupos': [], 'sin_sala': True})

    # Admin/Director ven todas
    grupos = Grupo.objects.select_related('educador_responsable').prefetch_related('ninos')
    return render(request, 'grupos/lista.html', {'grupos': grupos})

@login_required
def detalle_grupo(request, pk):
    rol = request.user.id_rol.nombre_rol if request.user.id_rol else ''

    # Educadora solo puede ver su propia sala
    if rol == ROL_EDUCADORA:
        grupo = get_object_or_404(Grupo, pk=pk, educador_responsable=request.user)
    else:
        grupo = get_object_or_404(Grupo, pk=pk)

    return render(request, 'grupos/detalle.html', {'grupo': grupo})

@login_required
def crear_grupo(request):
    form = GrupoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Grupo creado correctamente.')
        return redirect('grupos:lista_grupos')
    return render(request, 'grupos/form.html', {'form': form, 'titulo': 'Nuevo Grupo'})

@login_required
def editar_grupo(request, pk):
    grupo = get_object_or_404(Grupo, pk=pk)
    form = GrupoForm(request.POST or None, instance=grupo)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Grupo actualizado.')
        return redirect('grupos:lista_grupos')
    return render(request, 'grupos/form.html', {'form': form, 'titulo': 'Editar Grupo', 'objeto': grupo})

@login_required
def eliminar_grupo(request, pk):
    grupo = get_object_or_404(Grupo, pk=pk)
    if request.method == 'POST':
        grupo.delete()
        messages.success(request, 'Grupo eliminado.')
        return redirect('grupos:lista_grupos')
    return render(request, 'confirmar_eliminar.html', {'objeto': grupo, 'tipo': 'grupo'})