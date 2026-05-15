from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ItemInventario
from .forms import ItemInventarioForm
from grupos.models import Grupo

def _get_grupo_usuario(user):
    """Retorna el grupo asignado al educador, o None si no es educadora."""
    rol = user.id_rol.nombre_rol if user.id_rol else ''
    if rol == 'Educadora':
        return Grupo.objects.filter(educador_responsable=user).first()
    return None

@login_required
def lista_inventario(request):
    rol = request.user.id_rol.nombre_rol if request.user.id_rol else ''
    if rol == 'Educadora':
        grupo = _get_grupo_usuario(request.user)
        if not grupo:
            messages.warning(request, 'No tienes una sala asignada.')
            return render(request, 'inventario/lista.html', {'items': [], 'grupo': None})
        items = ItemInventario.objects.filter(grupo=grupo)
        grupos = [grupo]
    else:
        grupo_id = request.GET.get('grupo', '')
        grupos = Grupo.objects.all()
        items = ItemInventario.objects.select_related('grupo', 'registrado_por')
        if grupo_id:
            items = items.filter(grupo_id=grupo_id)
        grupo = Grupo.objects.filter(pk=grupo_id).first() if grupo_id else None

    estado_filtro = request.GET.get('estado', '')
    if estado_filtro:
        items = items.filter(estado=estado_filtro)

    return render(request, 'inventario/lista.html', {
        'items': items,
        'grupos': grupos,
        'grupo': grupo,
        'estado_filtro': estado_filtro,
    })

@login_required
def crear_item(request):
    rol = request.user.id_rol.nombre_rol if request.user.id_rol else ''
    grupo_educadora = _get_grupo_usuario(request.user) if rol == 'Educadora' else None

    form = ItemInventarioForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.registrado_por = request.user
        if grupo_educadora:
            item.grupo = grupo_educadora
        else:
            grupo_id = request.POST.get('grupo')
            if grupo_id:
                item.grupo = Grupo.objects.get(pk=grupo_id)
        item.save()
        messages.success(request, 'Ítem agregado al inventario.')
        return redirect('inventario:lista_inventario')

    grupos = Grupo.objects.all() if rol != 'Educadora' else []
    return render(request, 'inventario/form.html', {
        'form': form,
        'titulo': 'Nuevo Ítem',
        'grupos': grupos,
        'grupo_educadora': grupo_educadora,
    })

@login_required
def editar_item(request, pk):
    item = get_object_or_404(ItemInventario, pk=pk)
    form = ItemInventarioForm(request.POST or None, request.FILES or None, instance=item)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Ítem actualizado.')
        return redirect('inventario:lista_inventario')
    return render(request, 'inventario/form.html', {'form': form, 'titulo': 'Editar Ítem', 'objeto': item})

@login_required
def eliminar_item(request, pk):
    item = get_object_or_404(ItemInventario, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Ítem eliminado.')
        return redirect('inventario:lista_inventario')
    return render(request, 'confirmar_eliminar.html', {'objeto': item, 'tipo': 'ítem de inventario'})
