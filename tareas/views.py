
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import login as iniciar_sesion
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroForm, TareaForm
from .models import Tarea


from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def inicio(request):
    busqueda = request.GET.get('buscar', '')
    estado = request.GET.get('estado', '')

    tareas = Tarea.objects.filter(asignada_a=request.user)

    if busqueda:
        tareas = tareas.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

    if estado in ['pendiente', 'completada']:
        tareas = tareas.filter(estado=estado)

    tareas = tareas.order_by('-fecha_creacion')

    return render(request, 'tareas/inicio.html', {
        'tareas': tareas,
        'busqueda': busqueda,
        'estado_seleccionado': estado
    })



def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'tareas/registro.html', {
                'form': RegistroForm(),
                'mensaje': 'Usuario registrado correctamente.'
            })
    else:
        form = RegistroForm()

    return render(request, 'tareas/registro.html', {'form': form})


def iniciar_sesion_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            iniciar_sesion(request, form.get_user())
            return redirect('inicio')
    else:
        form = AuthenticationForm()

    return render(request, 'tareas/login.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')


@login_required(login_url='login')
def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)

        if form.is_valid():
    tarea = form.save(commit=False)

    if not tarea.asignada_a.is_active or tarea.asignada_a.is_staff or tarea.asignada_a.is_superuser:
        form.add_error('asignada_a', 'Solo se pueden asignar tareas a empleados activos.')

    else:
        tarea.creada_por = request.user
        tarea.save()
        return redirect('inicio')

            return redirect('inicio')
    else:
        form = TareaForm()

    return render(request, 'tareas/crear_tarea.html', {
        'form': form
    })


@login_required(login_url='login')
def editar_tarea(request, id):
    tarea = get_object_or_404(
        Tarea,
        id=id,
        asignada_a=request.user
    )

    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)

        if form.is_valid():
    tarea_actualizada = form.save(commit=False)

    if (
        not tarea_actualizada.asignada_a.is_active
        or tarea_actualizada.asignada_a.is_staff
        or tarea_actualizada.asignada_a.is_superuser
    ):
        form.add_error(
            'asignada_a',
            'Solo se pueden asignar tareas a empleados activos.'
        )
    else:
        tarea_actualizada.save()
        return redirect('inicio')
    else:
        form = TareaForm(instance=tarea)

    return render(request, 'tareas/editar_tarea.html', {
        'form': form,
        'tarea': tarea
    })


@login_required(login_url='login')
def eliminar_tarea(request, id):
    tarea = get_object_or_404(
        Tarea,
        id=id,
        asignada_a=request.user
    )

    if request.method == 'POST':
        tarea.delete()
        return redirect('inicio')

    return render(request, 'tareas/eliminar_tarea.html', {
        'tarea': tarea
    })


@login_required(login_url='login')
def cambiar_estado(request, id):
    tarea = get_object_or_404(
        Tarea,
        id=id,
        asignada_a=request.user
    )

    if request.method == 'POST':
        if tarea.estado == 'pendiente':
            tarea.estado = 'completada'
        else:
            tarea.estado = 'pendiente'

        tarea.save()

    return redirect('inicio')
