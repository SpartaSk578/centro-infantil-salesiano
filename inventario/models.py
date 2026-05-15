from django.db import models
from grupos.models import Grupo
from usuarios.models import Usuario

class ItemInventario(models.Model):
    ESTADO_CHOICES = [
        ('ALTA',    'Alta (Buen estado)'),
        ('REGULAR', 'Regular'),
        ('BAJA',    'Baja (Dañado/Perdido)'),
    ]

    TIPO_MOVIMIENTO_CHOICES = [
        ('DONACION', 'Donación'),
        ('COMPRA',   'Compra'),
        ('ROTURA',   'Rotura'),
        ('PERDIDA',  'Pérdida'),
        ('OTRO',     'Otro'),
    ]

    nombre          = models.CharField(max_length=150, verbose_name="Nombre del recurso")
    descripcion     = models.TextField(blank=True, null=True, verbose_name="Descripción")
    cantidad        = models.PositiveIntegerField(default=1)
    estado          = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='ALTA')
    tipo_movimiento = models.CharField(max_length=15, choices=TIPO_MOVIMIENTO_CHOICES, default='DONACION')
    grupo           = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='inventario')
    registrado_por  = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_registro  = models.DateTimeField(auto_now_add=True)
    foto1           = models.ImageField(upload_to='inventario/', blank=True, null=True)
    foto2           = models.ImageField(upload_to='inventario/', blank=True, null=True)
    foto3           = models.ImageField(upload_to='inventario/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.grupo} ({self.get_estado_display()})"

    class Meta:
        verbose_name = 'Ítem de Inventario'
        verbose_name_plural = 'Inventario'
        ordering = ['grupo', 'nombre']
