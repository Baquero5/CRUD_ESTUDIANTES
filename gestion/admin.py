from django.contrib import admin
from .models import Estudiante

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['cedula', 'nombres', 'apellidos', 'email', 'carrera', 'semestre', 'promedio', 'activo']
    list_filter = ['carrera', 'semestre', 'activo', 'fecha_registro']
    search_fields = ['cedula', 'nombres', 'apellidos', 'email']
    list_editable = ['activo']
    list_per_page = 20
    date_hierarchy = 'fecha_registro'
    ordering = ['-fecha_registro']