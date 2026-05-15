from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ninos', '0003_nino_ci_tutor_padre_alter_nino_ci_beneficiario'),
    ]

    operations = [
        # Datos antropométricos
        migrations.AddField(model_name='nino', name='peso_kg',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Peso (kg)'),
        ),
        migrations.AddField(model_name='nino', name='talla_cm',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Talla (cm)'),
        ),
        migrations.AddField(model_name='nino', name='estado_nutricional',
            field=models.CharField(blank=True, choices=[
                ('NORMAL','Normal'),('SOBREPESO','Sobrepeso'),('OBESIDAD','Obesidad'),
                ('DESNUT_AGUDA_MODERADA','Desnutrición Aguda Moderada'),
                ('DESNUT_AGUDA_GRAVE','Desnutrición Aguda Grave'),
                ('NO_TIENE_TALLA_BAJA','No tiene talla baja'),('TALLA_BAJA','Talla Baja'),
            ], max_length=30, null=True),
        ),
        migrations.AddField(model_name='nino', name='vacunas_al_dia',
            field=models.BooleanField(default=False, verbose_name='Vacunas al día'),
        ),
        # EAD
        migrations.AddField(model_name='nino', name='ead_motricidad_gruesa',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Motricidad Gruesa'),
        ),
        migrations.AddField(model_name='nino', name='ead_motricidad_fina',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Motricidad Fina'),
        ),
        migrations.AddField(model_name='nino', name='ead_audicion_lenguaje',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Audición y Lenguaje'),
        ),
        migrations.AddField(model_name='nino', name='ead_personal_social',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Personal y Social'),
        ),
        # Personas autorizadas
        migrations.AddField(model_name='nino', name='nombre_madre', field=models.CharField(blank=True, max_length=150, null=True)),
        migrations.AddField(model_name='nino', name='ci_madre', field=models.CharField(blank=True, max_length=20, null=True)),
        migrations.AddField(model_name='nino', name='nombre_padre', field=models.CharField(blank=True, max_length=150, null=True)),
        migrations.AddField(model_name='nino', name='ci_padre', field=models.CharField(blank=True, max_length=20, null=True)),
        migrations.AddField(model_name='nino', name='autorizado_1_nombre', field=models.CharField(blank=True, max_length=150, null=True)),
        migrations.AddField(model_name='nino', name='autorizado_1_ci', field=models.CharField(blank=True, max_length=20, null=True)),
        migrations.AddField(model_name='nino', name='autorizado_1_parentesco', field=models.CharField(blank=True, max_length=50, null=True)),
        migrations.AddField(model_name='nino', name='autorizado_2_nombre', field=models.CharField(blank=True, max_length=150, null=True)),
        migrations.AddField(model_name='nino', name='autorizado_2_ci', field=models.CharField(blank=True, max_length=20, null=True)),
        migrations.AddField(model_name='nino', name='autorizado_2_parentesco', field=models.CharField(blank=True, max_length=50, null=True)),
        migrations.AddField(model_name='nino', name='autorizado_3_nombre', field=models.CharField(blank=True, max_length=150, null=True)),
        migrations.AddField(model_name='nino', name='autorizado_3_ci', field=models.CharField(blank=True, max_length=20, null=True)),
        migrations.AddField(model_name='nino', name='autorizado_3_parentesco', field=models.CharField(blank=True, max_length=50, null=True)),
    ]
