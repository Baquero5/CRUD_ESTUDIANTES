from django.db import models

class Estudiante(models.Model):
    CARRERAS = [
        ('ISW', 'Ingeniería de Software'),
        ('ISI', 'Ingeniería en Sistemas'),
        ('IEC', 'Ingeniería en Computación'),
        ('ITE', 'Ingeniería en Telecomunicaciones'),
    ]
    
    cedula = models.CharField(max_length=10, unique=True, verbose_name='Cédula')
    nombres = models.CharField(max_length=100, verbose_name='Nombres')
    apellidos = models.CharField(max_length=100, verbose_name='Apellidos')
    email = models.EmailField(unique=True, verbose_name='Correo Electrónico')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    carrera = models.CharField(max_length=3, choices=CARRERAS, verbose_name='Carrera')
    semestre = models.IntegerField(verbose_name='Semestre')
    promedio = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Promedio')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')
    
    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cedula}"
    
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"