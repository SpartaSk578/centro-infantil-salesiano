from django.db import models
from django.core.validators import RegexValidator
from usuarios.models import Usuario

solo_letras = RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', "Solo letras.")
solo_numeros = RegexValidator(r'^\d+$', "Solo números.")

# Choices para Padres/IDS (Beneficiarios)
OCUPACION_CHOICES_BENEFICIARIO = [('ESTUDIANTE_IDTB', 'Estudiante IDTB')]

CARRERA_CHOICES = [
    ('CONTADURIA_GENERAL', 'Contaduría General'),
    ('ADMINISTRACION_EMPRESAS', 'Administración de Empresas'),
    ('SISTEMAS_COMPUTACIONALES', 'Sistemas Computacionales'),
    ('EDUCACION', 'Educación'),
    ('ENFERMERIA', 'Enfermería'),
    ('INGENIERIA_CIVIL', 'Ingeniería Civil'),
    ('INGENIERIA_INDUSTRIAL', 'Ingeniería Industrial'),
    ('PSICOLOGIA', 'Psicología'),
    ('DERECHO', 'Derecho'),
    ('INGLES', 'Inglés'),
    ('OTRO', 'Otra Carrera'),
]

# Choices para Padres/Externos (Tutores)
OCUPACION_CHOICES_TUTOR = [
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
]

# Mantener para compatibilidad
OCUPACION_CHOICES = [('ESTUDIANTE_IDTB', 'Estudiante IDTB'), ('OTRO', 'Otro')]
TURNO_CHOICES = [('MANANA', 'Mañana'), ('TARDE', 'Tarde'), ('NOCHE', 'Noche')]

class Beneficiario(models.Model):
    CI_beneficiario = models.CharField(max_length=15, primary_key=True)
    nombres = models.CharField(max_length=100, validators=[solo_letras])
    apellido_paterno = models.CharField(max_length=50, validators=[solo_letras])
    apellido_materno = models.CharField(max_length=50, validators=[solo_letras], blank=True)
    apellidos = models.CharField(max_length=100, blank=True, editable=False)
    ocupacion = models.CharField(max_length=30, choices=OCUPACION_CHOICES_BENEFICIARIO, default='ESTUDIANTE_IDTB')
    ocupacion_especifica = models.CharField(max_length=100, blank=True, null=True)
    carrera = models.CharField(max_length=100, blank=True, null=True)
    anio_semestre = models.CharField(max_length=50, blank=True, null=True)
    turno = models.CharField(max_length=15, choices=TURNO_CHOICES, blank=True, null=True)
    contacto = models.CharField(max_length=15, validators=[solo_numeros], blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    foto = models.ImageField(upload_to='beneficiarios/fotos/', blank=True, null=True)
    documento_adjunto = models.FileField(upload_to='beneficiarios/documentos/', blank=True, null=True)
    documentos_adjuntos = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def celular(self): return self.contacto

    def get_full_name(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}".strip()

    def __str__(self):
        return f"{self.get_full_name()} (CI: {self.CI_beneficiario})"

    def save(self, *args, **kwargs):
        self.apellidos = f"{self.apellido_paterno} {self.apellido_materno}".strip()
        super().save(*args, **kwargs)


class TutorPadre(models.Model):
    CI_tutor = models.CharField(max_length=15, primary_key=True)
    nombres = models.CharField(max_length=100, validators=[solo_letras])
    apellido_paterno = models.CharField(max_length=50, validators=[solo_letras])
    apellido_materno = models.CharField(max_length=50, validators=[solo_letras], blank=True)
    ocupacion = models.CharField(max_length=30, choices=OCUPACION_CHOICES_TUTOR, default='OTRO')
    ocupacion_especifica = models.CharField(max_length=100, blank=True, null=True)
    carrera = models.CharField(max_length=100, blank=True, null=True)
    anio_semestre = models.CharField(max_length=50, blank=True, null=True)
    turno = models.CharField(max_length=15, choices=TURNO_CHOICES, blank=True, null=True)
    contacto = models.CharField(max_length=15, validators=[solo_numeros], blank=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    foto = models.ImageField(upload_to='tutores/fotos/', blank=True, null=True)
    documento_adjunto = models.FileField(upload_to='tutores/documentos/', blank=True, null=True)
    documentos_adjuntos = models.TextField(blank=True, null=True)
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.SET_NULL, null=True, blank=True, related_name='tutores')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def celular(self): return self.contacto

    def get_full_name(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}".strip()

    def __str__(self):
        return f"{self.get_full_name()} (CI: {self.CI_tutor})"


SEXO_CHOICES = [('M', 'Masculino'), ('F', 'Femenino')]

class PreInscripcion(models.Model):
    ESTADOS = [('pendiente', 'Pendiente'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')]

    nombres_nino = models.CharField(max_length=100)
    apellido_paterno_nino = models.CharField(max_length=50, blank=True)
    apellido_materno_nino = models.CharField(max_length=50, blank=True)
    fecha_nacimiento_nino = models.DateField()
    sexo_nino = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    foto_nino = models.ImageField(upload_to='preinscripciones/fotos/', blank=True, null=True)
    sala_solicitada = models.CharField(max_length=50, blank=True, null=True)

    nombres_tutor = models.CharField(max_length=100)
    apellido_paterno_tutor = models.CharField(max_length=50, blank=True)
    apellido_materno_tutor = models.CharField(max_length=50, blank=True)
    CI_tutor = models.CharField(max_length=15, blank=True)
    ocupacion = models.CharField(max_length=30, choices=OCUPACION_CHOICES_TUTOR, default='OTRO')
    ocupacion_descripcion = models.CharField(max_length=100, blank=True, null=True)
    carrera = models.CharField(max_length=100, blank=True, null=True)
    anio_semestre = models.CharField(max_length=50, blank=True, null=True)
    turno = models.CharField(max_length=15, choices=TURNO_CHOICES, blank=True, null=True)
    telefono = models.CharField(max_length=15)

    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    observaciones_resolucion = models.TextField(blank=True, null=True)
    resuelto_por = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)

    def get_full_name_tutor(self):
        return f"{self.nombres_tutor} {self.apellido_paterno_tutor} {self.apellido_materno_tutor}".strip()

    def get_edad_anios(self):
        from datetime import date
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento_nino.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento_nino.month, self.fecha_nacimiento_nino.day):
            edad -= 1
        return edad

    def get_edad_meses(self):
        from datetime import date
        hoy = date.today()
        return (hoy.year - self.fecha_nacimiento_nino.year) * 12 + (hoy.month - self.fecha_nacimiento_nino.month)

    def get_meses_restantes(self):
        return self.get_edad_meses() % 12

    def __str__(self):
        return f"Pre-inscripción: {self.nombres_nino} {self.apellido_paterno_nino}"

    class Meta:
        verbose_name = 'Pre-inscripción'
        verbose_name_plural = 'Pre-inscripciones'