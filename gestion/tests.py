from django.test import TestCase, Client
from django.urls import reverse
from .models import Estudiante
from datetime import date

class EstudianteModelTest(TestCase):
    """Pruebas para el modelo Estudiante"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.estudiante = Estudiante.objects.create(
            cedula='1234567890',
            nombres='Juan Carlos',
            apellidos='Pérez López',
            email='juan.perez@test.com',
            fecha_nacimiento=date(2000, 5, 15),
            carrera='ISW',
            semestre=5,
            promedio=8.50,
            activo=True
        )
    
    def test_estudiante_creation(self):
        """Verifica que se pueda crear un estudiante"""
        self.assertEqual(self.estudiante.cedula, '1234567890')
        self.assertEqual(self.estudiante.nombres, 'Juan Carlos')
        self.assertTrue(isinstance(self.estudiante, Estudiante))
    
    def test_estudiante_str(self):
        """Verifica el método __str__ del estudiante"""
        expected = "Juan Carlos Pérez López - 1234567890"
        self.assertEqual(str(self.estudiante), expected)
    
    def test_nombre_completo(self):
        """Verifica el método nombre_completo"""
        expected = "Juan Carlos Pérez López"
        self.assertEqual(self.estudiante.nombre_completo(), expected)
    
    def test_cedula_unique(self):
        """Verifica que la cédula sea única"""
        with self.assertRaises(Exception):
            Estudiante.objects.create(
                cedula='1234567890',  # Cédula duplicada
                nombres='María',
                apellidos='González',
                email='maria@test.com',
                fecha_nacimiento=date(2001, 3, 10),
                carrera='ISI',
                semestre=3,
                promedio=7.50,
                activo=True
            )


class EstudianteViewsTest(TestCase):
    """Pruebas para las vistas de Estudiante"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        self.estudiante = Estudiante.objects.create(
            cedula='0987654321',
            nombres='Ana',
            apellidos='Martínez',
            email='ana.martinez@test.com',
            fecha_nacimiento=date(1999, 8, 20),
            carrera='IEC',
            semestre=6,
            promedio=9.00,
            activo=True
        )
    
    def test_estudiante_list_view(self):
        """Verifica que la vista de listado funcione"""
        response = self.client.get(reverse('estudiante_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ana')
        self.assertContains(response, 'Martínez')
    
    def test_estudiante_detail_view(self):
        """Verifica que la vista de detalle funcione"""
        response = self.client.get(
            reverse('estudiante_detail', args=[self.estudiante.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '0987654321')
    
    def test_estudiante_create_view_get(self):
        """Verifica que el formulario de creación se muestre"""
        response = self.client.get(reverse('estudiante_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Crear')
    
    def test_estudiante_create_view_post(self):
        """Verifica que se pueda crear un estudiante vía POST"""
        data = {
            'cedula': '1111111111',
            'nombres': 'Pedro',
            'apellidos': 'Ramírez',
            'email': 'pedro@test.com',
            'fecha_nacimiento': '2000-01-01',
            'carrera': 'ITE',
            'semestre': 4,
            'promedio': 7.75,
            'activo': True
        }
        response = self.client.post(reverse('estudiante_create'), data)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Estudiante.objects.count(), 2)
    
    def test_estudiante_update_view(self):
        """Verifica que se pueda actualizar un estudiante"""
        data = {
            'cedula': '0987654321',
            'nombres': 'Ana María',
            'apellidos': 'Martínez Silva',
            'email': 'ana.martinez@test.com',
            'fecha_nacimiento': '1999-08-20',
            'carrera': 'IEC',
            'semestre': 7,
            'promedio': 9.25,
            'activo': True
        }
        response = self.client.post(
            reverse('estudiante_update', args=[self.estudiante.pk]), 
            data
        )
        self.assertEqual(response.status_code, 302)
        self.estudiante.refresh_from_db()
        self.assertEqual(self.estudiante.nombres, 'Ana María')
    
    def test_estudiante_delete_view(self):
        """Verifica que se pueda eliminar un estudiante"""
        response = self.client.post(
            reverse('estudiante_delete', args=[self.estudiante.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Estudiante.objects.count(), 0)
    
    def test_estudiante_search(self):
        """Verifica la funcionalidad de búsqueda"""
        response = self.client.get(reverse('estudiante_list'), {'q': 'Ana'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ana')


class EstudianteFormTest(TestCase):
    """Pruebas para los formularios"""
    
    def test_valid_form(self):
        """Verifica que un formulario válido se acepte"""
        from .forms import EstudianteForm
        data = {
            'cedula': '2222222222',
            'nombres': 'Luis',
            'apellidos': 'García',
            'email': 'luis@test.com',
            'fecha_nacimiento': '1998-12-25',
            'carrera': 'ISW',
            'semestre': 8,
            'promedio': 8.00,
            'activo': True
        }
        form = EstudianteForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_cedula_length(self):
        """Verifica validación de cédula con longitud incorrecta"""
        from .forms import EstudianteForm
        data = {
            'cedula': '123',  # Muy corta
            'nombres': 'Luis',
            'apellidos': 'García',
            'email': 'luis@test.com',
            'fecha_nacimiento': '1998-12-25',
            'carrera': 'ISW',
            'semestre': 8,
            'promedio': 8.00,
            'activo': True
        }
        form = EstudianteForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('cedula', form.errors)
    
    def test_invalid_semestre(self):
        """Verifica validación de semestre fuera de rango"""
        from .forms import EstudianteForm
        data = {
            'cedula': '3333333333',
            'nombres': 'María',
            'apellidos': 'López',
            'email': 'maria@test.com',
            'fecha_nacimiento': '2000-06-15',
            'carrera': 'ISI',
            'semestre': 15,  # Fuera de rango
            'promedio': 7.50,
            'activo': True
        }
        form = EstudianteForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('semestre', form.errors)