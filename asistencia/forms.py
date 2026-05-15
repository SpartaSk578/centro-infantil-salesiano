from django import forms
from .models import Asistencia

class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['fecha', 'estado', 'tipo_permiso', 'observaciones', 'id_nino']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'tipo_permiso': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'id_nino': forms.Select(attrs={'class': 'form-select'}),
        }

class AsistenciaMasivaForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    grupo = forms.IntegerField(required=False, widget=forms.HiddenInput())
