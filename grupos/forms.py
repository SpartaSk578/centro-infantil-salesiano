from django import forms
from .models import Grupo
from usuarios.models import Usuario, Rol

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nombre_grupo', 'educador_responsable']
        widgets = {'nombre_grupo': forms.TextInput(attrs={'class': 'form-control'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['educador_responsable'].widget.attrs['class'] = 'form-select'
        from django.db.models import Q
        roles_educadores = Rol.objects.filter(Q(nombre_rol='Educador') | Q(nombre_rol='Educadora'))
        self.fields['educador_responsable'].queryset = Usuario.objects.filter(id_rol__in=roles_educadores, estado='activo')
