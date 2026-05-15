from django import forms
from .models import Nino, DocumentoNino

class NinoForm(forms.ModelForm):
    class Meta:
        model = Nino
        fields = [
            'nombres', 'apellido_paterno', 'apellido_materno', 'ci_nino', 'sexo',
            'fecha_nacimiento', 'fecha_ingreso', 'direccion', 'sala', 'id_grupo', 'foto',
            # Antropométricos
            'peso_kg', 'talla_cm', 'estado_nutricional', 'vacunas_al_dia',
            # EAD
            'ead_motricidad_gruesa', 'ead_motricidad_fina', 'ead_audicion_lenguaje', 'ead_personal_social',
            # Médico
            'info_medica',
            # Responsables
            'CI_beneficiario', 'CI_tutor_padre',
            # Personas autorizadas
            'nombre_madre', 'ci_madre', 'nombre_padre', 'ci_padre',
            'autorizado_1_nombre', 'autorizado_1_ci', 'autorizado_1_parentesco',
            'autorizado_2_nombre', 'autorizado_2_ci', 'autorizado_2_parentesco',
            'autorizado_3_nombre', 'autorizado_3_ci', 'autorizado_3_parentesco',
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'ci_nino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 17957806'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zona / Calle / Nº'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'sala': forms.Select(attrs={'class': 'form-select'}),
            'id_grupo': forms.Select(attrs={'class': 'form-select'}),
            'peso_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Ej: 12.5'}),
            'talla_cm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Ej: 85.0'}),
            'estado_nutricional': forms.Select(attrs={'class': 'form-select'}),
            'vacunas_al_dia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ead_motricidad_gruesa': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'ead_motricidad_fina': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'ead_audicion_lenguaje': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'ead_personal_social': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'info_medica': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'CI_beneficiario': forms.Select(attrs={'class': 'form-select'}),
            'CI_tutor_padre': forms.Select(attrs={'class': 'form-select'}),
            'nombre_madre': forms.TextInput(attrs={'class': 'form-control'}),
            'ci_madre': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_padre': forms.TextInput(attrs={'class': 'form-control'}),
            'ci_padre': forms.TextInput(attrs={'class': 'form-control'}),
            'autorizado_1_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'autorizado_1_ci': forms.TextInput(attrs={'class': 'form-control'}),
            'autorizado_1_parentesco': forms.TextInput(attrs={'class': 'form-control'}),
            'autorizado_2_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'autorizado_2_ci': forms.TextInput(attrs={'class': 'form-control'}),
            'autorizado_2_parentesco': forms.TextInput(attrs={'class': 'form-control'}),
            'autorizado_3_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'autorizado_3_ci': forms.TextInput(attrs={'class': 'form-control'}),
            'autorizado_3_parentesco': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DocumentoNinoForm(forms.ModelForm):
    class Meta:
        model = DocumentoNino
        fields = ['nombre', 'archivo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }
