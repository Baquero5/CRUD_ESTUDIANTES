from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Estudiante
from .forms import EstudianteForm

# READ - Listar todos los estudiantes
def estudiante_list(request):
    query = request.GET.get('q')
    if query:
        estudiantes = Estudiante.objects.filter(
            Q(nombres__icontains=query) | 
            Q(apellidos__icontains=query) | 
            Q(cedula__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        estudiantes = Estudiante.objects.all()
    
    context = {
        'estudiantes': estudiantes,
        'query': query
    }
    return render(request, 'gestion/estudiante_list.html', context)

# READ - Ver detalle de un estudiante
def estudiante_detail(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    context = {
        'estudiante': estudiante
    }
    return render(request, 'gestion/estudiante_detail.html', context)

# CREATE - Crear nuevo estudiante
def estudiante_create(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Estudiante creado exitosamente!')
            return redirect('estudiante_list')
    else:
        form = EstudianteForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Nuevo Estudiante',
        'boton': 'Crear'
    }
    return render(request, 'gestion/estudiante_form.html', context)

# UPDATE - Actualizar estudiante existente
def estudiante_update(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    if request.method == 'POST':
        form = EstudianteForm(request.POST, instance=estudiante)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Estudiante actualizado exitosamente!')
            return redirect('estudiante_detail', pk=estudiante.pk)
    else:
        form = EstudianteForm(instance=estudiante)
    
    context = {
        'form': form,
        'titulo': 'Actualizar Estudiante',
        'boton': 'Actualizar',
        'estudiante': estudiante
    }
    return render(request, 'gestion/estudiante_form.html', context)

# DELETE - Eliminar estudiante
def estudiante_delete(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    if request.method == 'POST':
        estudiante.delete()
        messages.success(request, '¡Estudiante eliminado exitosamente!')
        return redirect('estudiante_list')
    
    context = {
        'estudiante': estudiante
    }
    return render(request, 'gestion/estudiante_confirm_delete.html', context)