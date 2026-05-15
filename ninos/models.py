from django.db import models
from django.core.validators import RegexValidator
from usuarios.models import Usuario
from beneficiarios.models import Beneficiario
from grupos.models import Grupo

solo_letras_nino = RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', "Solo se permiten letras.")

class Nino(models.Model):
    MASCULINO = 'M'
    FEMENINO = 'F'
    SEXO_CHOICES = [(MASCULINO, 'Masculino'), (FEMENINO, 'Femenino')]

    LACTANTES = 'LACTANTES'
    INFANTE_I = 'INFANTE I'
    INFANTE_II_A = 'INFANTE II A'
    INFANTE_II_B = 'INFANTE II B'
    SALA_CHOICES = [
        (LACTANTES, 'Lactantes'),
        (INFANTE_I, 'Infante I'),
        (INFANTE_II_A, 'Infante II A'),
        (INFANTE_II_B, 'Infante II B'),
    ]

    ESTADO_NUTRICIONAL_CHOICES = [
        ('NORMAL', 'Normal'),
        ('SOBREPESO', 'Sobrepeso'),
        ('OBESIDAD', 'Obesidad'),
        ('DESNUT_AGUDA_MODERADA', 'Desnutrición Aguda Moderada'),
        ('DESNUT_AGUDA_GRAVE', 'Desnutrición Aguda Grave'),
        ('NO_TIENE_TALLA_BAJA', 'No tiene talla baja'),
        ('TALLA_BAJA', 'Talla Baja'),
    ]

    # Datos básicos
    nombres = models.CharField(max_length=100, validators=[solo_letras_nino])
    apellido_paterno = models.CharField(max_length=50, validators=[solo_letras_nino])
    apellido_materno = models.CharField(max_length=50, validators=[solo_letras_nino], blank=True)
    apellidos = models.CharField(max_length=100, blank=True, editable=False)
    ci_nino = models.CharField(max_length=20, blank=True, null=True, verbose_name='CI del Niño/a')
    direccion = models.CharField(max_length=200, blank=True, null=True, verbose_name='Dirección')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    fecha_nacimiento = models.DateField()
    sala = models.CharField(max_length=20, choices=SALA_CHOICES, blank=True, null=True)
    foto = models.ImageField(upload_to='ninos/fotos/', blank=True, null=True)
    fecha_ingreso = models.DateField()

    # Datos antropométricos
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    talla_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Talla (cm)")
    estado_nutricional = models.CharField(max_length=30, choices=ESTADO_NUTRICIONAL_CHOICES, blank=True, null=True)

    # Vacunas
    vacunas_al_dia = models.BooleanField(default=False, verbose_name="Vacunas al día")

    # Escala abreviada de desarrollo
    ead_motricidad_gruesa = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Motricidad Gruesa")
    ead_motricidad_fina = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Motricidad Fina")
    ead_audicion_lenguaje = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Audición y Lenguaje")
    ead_personal_social = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Personal y Social")

    # Información médica
    info_medica = models.TextField(blank=True, null=True, verbose_name="Información Médica")

    # Personas autorizadas
    nombre_madre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre de la Madre")
    ci_madre = models.CharField(max_length=20, blank=True, null=True, verbose_name="CI Madre")
    nombre_padre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre del Padre")
    ci_padre = models.CharField(max_length=20, blank=True, null=True, verbose_name="CI Padre")
    autorizado_1_nombre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Autorizado 1 - Nombre")
    autorizado_1_ci = models.CharField(max_length=20, blank=True, null=True, verbose_name="Autorizado 1 - CI")
    autorizado_1_parentesco = models.CharField(max_length=50, blank=True, null=True, verbose_name="Autorizado 1 - Parentesco")
    autorizado_2_nombre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Autorizado 2 - Nombre")
    autorizado_2_ci = models.CharField(max_length=20, blank=True, null=True, verbose_name="Autorizado 2 - CI")
    autorizado_2_parentesco = models.CharField(max_length=50, blank=True, null=True, verbose_name="Autorizado 2 - Parentesco")
    autorizado_3_nombre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Autorizado 3 - Nombre")
    autorizado_3_ci = models.CharField(max_length=20, blank=True, null=True, verbose_name="Autorizado 3 - CI")
    autorizado_3_parentesco = models.CharField(max_length=50, blank=True, null=True, verbose_name="Autorizado 3 - Parentesco")

    # Relaciones
    CI_beneficiario = models.ForeignKey(Beneficiario, on_delete=models.PROTECT, related_name='ninos', null=True, blank=True)
    CI_tutor_padre = models.ForeignKey('beneficiarios.TutorPadre', on_delete=models.PROTECT, related_name='ninos', null=True, blank=True)
    registrado_por = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='ninos_registrados')
    id_grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null=True, blank=True, related_name='ninos')

    def save(self, *args, **kwargs):
        self.apellidos = f"{self.apellido_paterno} {self.apellido_materno}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    def get_full_name(self):
        return f"{self.nombres} {self.apellidos}".strip()

    @property
    def responsable(self):
        return self.CI_beneficiario or self.CI_tutor_padre

    def get_responsable_name(self):
        resp = self.responsable
        return resp.get_full_name() if resp else "Sin tutor"

    def get_edad(self):
        from datetime import date
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad

    def get_edad_meses(self):
        from datetime import date
        hoy = date.today()
        return (hoy.year - self.fecha_nacimiento.year) * 12 + (hoy.month - self.fecha_nacimiento.month)

    def get_meses_restantes(self):
        return self.get_edad_meses() % 12

    def get_edad_display(self):
        from datetime import date
        hoy = date.today()
        anios = hoy.year - self.fecha_nacimiento.year
        meses = hoy.month - self.fecha_nacimiento.month
        if hoy.day < self.fecha_nacimiento.day:
            meses -= 1
        if meses < 0:
            anios -= 1
            meses += 12
        if anios > 0:
            return f"{anios} años, {meses} m" if meses > 0 else f"{anios} años"
        return f"{meses} meses"

    @property
    def ead_total(self):
        vals = [self.ead_motricidad_gruesa, self.ead_motricidad_fina,
                self.ead_audicion_lenguaje, self.ead_personal_social]
        vals = [v for v in vals if v is not None]
        return sum(vals) if vals else None

    class Meta:
        verbose_name = 'Niño'
        verbose_name_plural = 'Niños'
        ordering = ['apellido_paterno', 'apellido_materno', 'nombres']


class DocumentoNino(models.Model):
    nino = models.ForeignKey(Nino, on_delete=models.CASCADE, related_name='documentos')
    nombre = models.CharField(max_length=100, verbose_name="Nombre del documento")
    archivo = models.FileField(upload_to='ninos/documentos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.nino}"

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
