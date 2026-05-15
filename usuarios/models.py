from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator

# Validadores
solo_letras = RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', "Este campo no puede contener números.")
solo_numeros = RegexValidator(r'^\d+$', "El teléfono solo debe contener números.")

class Rol(models.Model):
    # Eliminamos las constantes y choices para permitir total flexibilidad desde el Admin
    nombre_rol = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.nombre_rol)

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_usuario, email, password=None, **extra):
        if not email:
            raise ValueError('El email es requerido')
        email = self.normalize_email(email)
        user = self.model(nombre_usuario=nombre_usuario, email=email, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_usuario, email, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('is_active', True)
        return self.create_user(nombre_usuario, email, password, **extra)

class Usuario(AbstractBaseUser, PermissionsMixin):
    ACTIVO = 'activo'
    INACTIVO = 'inactivo'
    ESTADOS = [(ACTIVO, 'Activo'), (INACTIVO, 'Inactivo')]

    nombre_usuario = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    nombres = models.CharField(max_length=100, blank=True, validators=[solo_letras])
    apellidos = models.CharField(max_length=100, blank=True, validators=[solo_letras])
    telefono = models.CharField(max_length=20, blank=True, null=True, validators=[solo_numeros])
    foto_perfil = models.ImageField(upload_to='usuarios/fotos/', blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default=ACTIVO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultimo_acceso = models.DateTimeField(null=True, blank=True)
    id_rol = models.ForeignKey(Rol, on_delete=models.PROTECT, null=True, blank=True, related_name='usuarios')
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'nombre_usuario'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        rol_nombre = self.id_rol.nombre_rol if self.id_rol else "Sin Rol"
        return f"{self.nombre_usuario} ({rol_nombre})"

    def get_full_name(self):
        full_name = f"{self.nombres} {self.apellidos}".strip()
        return full_name if full_name else self.nombre_usuario

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'