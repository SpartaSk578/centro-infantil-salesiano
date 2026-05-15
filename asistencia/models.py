from django.db import models
from ninos.models import Nino
from usuarios.models import Usuario

class Asistencia(models.Model):
    # Estados principales
    ASISTIO   = 'asistio'
    FALTO     = 'falto'
    PERMISO   = 'permiso'

    ESTADO_CHOICES = [
        (ASISTIO, 'Asistió'),
        (FALTO,   'Faltó'),
        (PERMISO, 'Permiso'),
    ]

    # Tipos de permiso
    PERMISO_RESFRIO  = 'PR'
    PERMISO_DIARREA  = 'PD'
    PERMISO_VIAJE    = 'PV'
    PERMISO_MALTRATO = 'M'
    PERMISO_OTRO     = 'PO'

    TIPO_PERMISO_CHOICES = [
        (PERMISO_RESFRIO,  'Resfrío (PR)'),
        (PERMISO_DIARREA,  'Diarrea (PD)'),
        (PERMISO_VIAJE,    'Viaje (PV)'),
        (PERMISO_MALTRATO, 'Maltrato (M)'),
        (PERMISO_OTRO,     'Otro'),
    ]

    fecha           = models.DateField()
    estado          = models.CharField(max_length=10, choices=ESTADO_CHOICES, default=ASISTIO)
    tipo_permiso    = models.CharField(max_length=5, choices=TIPO_PERMISO_CHOICES, blank=True, null=True)
    observaciones   = models.TextField(blank=True, null=True)
    id_nino         = models.ForeignKey(Nino, on_delete=models.CASCADE, related_name='asistencias')
    registrado_por  = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='asistencias_registradas')

    def get_simbolo(self):
        if self.estado == self.ASISTIO:
            return '●'
        elif self.estado == self.FALTO:
            return '✗'
        elif self.estado == self.PERMISO:
            return self.tipo_permiso or 'P'
        return '?'

    def get_color_clase(self):
        if self.estado == self.ASISTIO:
            return 'success'
        elif self.estado == self.FALTO:
            return 'danger'
        elif self.estado == self.PERMISO:
            return 'warning'
        return 'secondary'

    # Compatibilidad con código anterior
    @property
    def presente(self):
        return self.estado == self.ASISTIO

    def __str__(self):
        return f"{self.id_nino} - {self.fecha} - {self.get_simbolo()}"

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['-fecha']
        unique_together = ['fecha', 'id_nino']
