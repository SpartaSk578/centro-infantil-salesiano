from django import forms
from .models import Evaluacion

class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['id_nino', 'fecha', 'periodo', 'motricidad_gruesa', 'motricidad_fina',
                  'audicion_lenguaje', 'personal_social', 'peso_kg', 'talla_cm',
                  'clasificacion', 'resultados']
        widgets = {
            'id_nino': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'periodo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Enero 2026'}),
            'motricidad_gruesa': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'motricidad_fina': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'audicion_lenguaje': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'personal_social': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'peso_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'talla_cm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'clasificacion': forms.Select(attrs={'class': 'form-select'}),
            'resultados': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
