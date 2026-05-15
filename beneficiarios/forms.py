from django import forms
from .models import Beneficiario, TutorPadre, PreInscripcion, CARRERA_CHOICES


class BeneficiarioForm(forms.ModelForm):
    """Formulario para Padres/IDS (Beneficiarios) - Solo carrera"""
    carrera = forms.ChoiceField(
        choices=[('', '--- Selecciona una carrera ---')] + CARRERA_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text='O especifica manualmente'  
    )
    carrera_manual = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Si es otra carrera, especifica aquí'})
    )
    class Meta:
        model = Beneficiario
        fields = ['CI_beneficiario', 'nombres', 'apellido_paterno', 'apellido_materno',
                  'carrera', 'anio_semestre', 'turno',
                  'contacto', 'direccion', 'foto', 'documento_adjunto', 'documentos_adjuntos']
        labels = {
            'CI_beneficiario': 'CI PADRE/IDS',
        }
        widgets = {
            'CI_beneficiario': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'carrera': forms.Select(attrs={'class': 'form-select'}),
            'anio_semestre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 3er Año'}),
            'turno': forms.Select(attrs={'class': 'form-select'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'id': 'id_foto'}),
            'documento_adjunto': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png', 'id': 'id_documento_adjunto'}),
            'documentos_adjuntos': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notas adicionales...'}),
        }


class TutorPadreForm(forms.ModelForm):
    """Formulario para Padres/Externos (Tutores) - Solo ocupación"""
    class Meta:
        model = TutorPadre
        fields = ['CI_tutor', 'nombres', 'apellido_paterno', 'apellido_materno',
                  'ocupacion', 'ocupacion_especifica',
                  'contacto', 'direccion', 'foto', 'documento_adjunto', 'documentos_adjuntos']
        widgets = {
            'CI_tutor': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'ocupacion': forms.Select(attrs={'class': 'form-select'}),
            'ocupacion_especifica': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especificar ocupación (si es "Otro")'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'id': 'id_tutor_foto'}),
            'documento_adjunto': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png', 'id': 'id_tutor_documento'}),
            'documentos_adjuntos': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notas adicionales...'}),
        }


class PreInscripcionForm(forms.ModelForm):
    class Meta:
        model = PreInscripcion
        fields = [
            'nombres_nino', 'apellido_paterno_nino', 'apellido_materno_nino',
            'fecha_nacimiento_nino', 'sexo_nino', 'sala_solicitada', 'foto_nino',
            'nombres_tutor', 'apellido_paterno_tutor', 'apellido_materno_tutor',
            'CI_tutor', 'ocupacion', 'telefono',
        ]
        widgets = {
            'fecha_nacimiento_nino': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nombres_nino': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno_nino': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno_nino': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo_nino': forms.Select(attrs={'class': 'form-select'}),
            'sala_solicitada': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Lactantes, Infante I...'}),
            'foto_nino': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*', 'id': 'id_foto'}),
            'nombres_tutor': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno_tutor': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno_tutor': forms.TextInput(attrs={'class': 'form-control'}),
            'CI_tutor': forms.TextInput(attrs={'class': 'form-control'}),
            'ocupacion': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('COSTURA', 'Costura'),
                ('ALBAÑIL', 'Albañil'),
                ('COMERCIANTE', 'Comerciante'),
                ('EMPLEADO', 'Empleado'),
                ('OBRERO', 'Obrero'),
                ('PROFESIONAL', 'Profesional'),
                ('VENDEDOR', 'Vendedor'),
                ('ARTESANO', 'Artesano'),
                ('TRANSPORTISTA', 'Transportista'),
                ('AGRICULTOR', 'Agricultor'),
                ('OTRO', 'Otro'),
            ]),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }