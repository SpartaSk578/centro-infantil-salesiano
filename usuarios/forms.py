from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario, Rol

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

class UsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'email', 'nombres', 'apellidos', 'id_rol', 'estado']
        widgets = {f: forms.TextInput(attrs={'class': 'form-control'}) for f in ['nombre_usuario', 'nombres', 'apellidos']}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['id_rol'].widget.attrs['class'] = 'form-select'
        self.fields['estado'].widget.attrs['class'] = 'form-select'
        
        # Si estamos creando (no hay instancia con PK), pedimos contraseña
        if not self.instance.pk:
            self.fields['password1'].required = True
            self.fields['password2'].required = True

    def clean(self):
        cd = super().clean()
        p1, p2 = cd.get('password1'), cd.get('password2')
        
        # Solo validar coincidencia si se ingresó algo o si es obligatorio
        if (p1 or p2) and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
