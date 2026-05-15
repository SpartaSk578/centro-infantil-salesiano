from django.db import models
from usuarios.models import Usuario

class Grupo(models.Model):
    nombre_grupo = models.CharField(max_length=50)
    educador_responsable = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='grupos_a_cargo')

    def __str__(self):
        return self.nombre_grupo

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['nombre_grupo']
