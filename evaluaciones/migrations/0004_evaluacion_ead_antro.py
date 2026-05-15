from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluaciones', '0003_initial'),
    ]

    operations = [
        # EAD fields
        migrations.AddField(model_name='evaluacion', name='motricidad_gruesa',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Motricidad Gruesa'),
        ),
        migrations.AddField(model_name='evaluacion', name='motricidad_fina',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Motricidad Fina'),
        ),
        migrations.AddField(model_name='evaluacion', name='audicion_lenguaje',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Audición y Lenguaje'),
        ),
        migrations.AddField(model_name='evaluacion', name='personal_social',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Personal y Social'),
        ),
        # Anthropometric fields
        migrations.AddField(model_name='evaluacion', name='peso_kg',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Peso (kg)'),
        ),
        migrations.AddField(model_name='evaluacion', name='talla_cm',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Talla (cm)'),
        ),
        # Update clasificacion to have proper choices
        migrations.AlterField(
            model_name='evaluacion',
            name='clasificacion',
            field=models.CharField(
                blank=True,
                choices=[
                    ('ALTO', 'Alto (Azul)'),
                    ('MEDIO_ALTO', 'Medio Alto (Verde)'),
                    ('MEDIO_BAJO', 'Medio Bajo (Amarillo)'),
                    ('ALERTA', 'Alerta (Rojo)'),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
