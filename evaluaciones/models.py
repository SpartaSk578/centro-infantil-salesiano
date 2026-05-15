from django.db import models
from ninos.models import Nino
from usuarios.models import Usuario

class Evaluacion(models.Model):
    CLASIFICACION_CHOICES = [
        ('ALTO',        'Alto (Azul)'),
        ('MEDIO_ALTO',  'Medio Alto (Verde)'),
        ('MEDIO_BAJO',  'Medio Bajo (Amarillo)'),
        ('ALERTA',      'Alerta (Rojo)'),
    ]

    fecha           = models.DateField()
    periodo         = models.CharField(max_length=50, blank=True, null=True, verbose_name="Período")
    # Escala abreviada de desarrollo
    motricidad_gruesa   = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Motricidad Gruesa")
    motricidad_fina     = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Motricidad Fina")
    audicion_lenguaje   = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Audición y Lenguaje")
    personal_social     = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Personal y Social")
    # Datos antropométricos del período
    peso_kg     = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    talla_cm    = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Talla (cm)")
    clasificacion   = models.CharField(max_length=20, choices=CLASIFICACION_CHOICES, blank=True, null=True)
    resultados      = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    id_nino         = models.ForeignKey(Nino, on_delete=models.CASCADE, related_name='evaluaciones')
    registrado_por  = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='evaluaciones_registradas')

    @property
    def total_puntaje(self):
        vals = [self.motricidad_gruesa, self.motricidad_fina,
                self.audicion_lenguaje, self.personal_social]
        vals = [v for v in vals if v is not None]
        return sum(vals) if vals else None

    def get_color_clasificacion(self):
        colores = {
            'ALTO': '#2563EB',
            'MEDIO_ALTO': '#16A34A',
            'MEDIO_BAJO': '#D97706',
            'ALERTA': '#DC2626',
        }
        return colores.get(self.clasificacion, '#64748B')

    def __str__(self):
        return f"{self.id_nino} - {self.periodo} - {self.clasificacion}"

    class Meta:
        verbose_name = 'Evaluación'
        verbose_name_plural = 'Evaluaciones'
        ordering = ['-fecha']
