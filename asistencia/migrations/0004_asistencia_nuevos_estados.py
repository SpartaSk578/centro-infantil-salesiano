from django.db import migrations, models


def migrar_estados(apps, schema_editor):
    """Convierte estados antiguos (presente/ausente) a nuevos (asistio/falto)"""
    Asistencia = apps.get_model('asistencia', 'Asistencia')
    Asistencia.objects.filter(estado='presente').update(estado='asistio')
    Asistencia.objects.filter(estado='ausente').update(estado='falto')


class Migration(migrations.Migration):

    dependencies = [
        ('asistencia', '0003_initial'),
    ]

    operations = [
        # Primero ampliar el campo para aceptar los nuevos valores
        migrations.AlterField(
            model_name='asistencia',
            name='estado',
            field=models.CharField(
                choices=[
                    ('presente', 'Presente'),
                    ('ausente', 'Ausente'),
                    ('asistio', 'Asistió'),
                    ('falto', 'Faltó'),
                    ('permiso', 'Permiso'),
                ],
                default='asistio',
                max_length=10,
            ),
        ),
        # Migrar datos existentes
        migrations.RunPython(migrar_estados, migrations.RunPython.noop),
        # Establecer los choices finales
        migrations.AlterField(
            model_name='asistencia',
            name='estado',
            field=models.CharField(
                choices=[('asistio', 'Asistió'), ('falto', 'Faltó'), ('permiso', 'Permiso')],
                default='asistio',
                max_length=10,
            ),
        ),
        # Agregar campo tipo_permiso
        migrations.AddField(
            model_name='asistencia',
            name='tipo_permiso',
            field=models.CharField(
                blank=True,
                choices=[
                    ('PR', 'Resfrío (PR)'),
                    ('PD', 'Diarrea (PD)'),
                    ('PV', 'Viaje (PV)'),
                    ('M',  'Maltrato (M)'),
                    ('PO', 'Otro'),
                ],
                max_length=5,
                null=True,
            ),
        ),
    ]
