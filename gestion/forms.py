from django import forms
from .models import Estudiante

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['cedula', 'nombres', 'apellidos', 'email', 'fecha_nacimiento', 
                  'carrera', 'semestre', 'promedio', 'activo']
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234567890'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombres'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'carrera': forms.Select(attrs={'class': 'form-control'}),
            'semestre': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'promedio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '10'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if len(cedula) != 10:
            raise forms.ValidationError('La cédula debe tener 10 dígitos')
        if not cedula.isdigit():
            raise forms.ValidationError('La cédula solo debe contener números')
        return cedula
    
    def clean_semestre(self):
        semestre = self.cleaned_data.get('semestre')
        if semestre < 1 or semestre > 10:
            raise forms.ValidationError('El semestre debe estar entre 1 y 10')
        return semestre
    
    def clean_promedio(self):
        promedio = self.cleaned_data.get('promedio')
        if promedio < 0 or promedio > 10:
            raise forms.ValidationError('El promedio debe estar entre 0 y 10')
        return promedio