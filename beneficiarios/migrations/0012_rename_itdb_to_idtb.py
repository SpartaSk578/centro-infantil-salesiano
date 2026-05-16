from django.db import migrations


def rename_itdb_to_itdb(apps, schema_editor):
    Beneficiario = apps.get_model('beneficiarios', 'Beneficiario')
    Beneficiario.objects.filter(ocupacion='ESTUDIANTE_ITDB').update(ocupacion='ESTUDIANTE_ITDB')


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiarios', '0011_alter_beneficiario_ocupacion_and_more'),
    ]

    operations = [
        migrations.RunPython(rename_itdb_to_itdb, migrations.RunPython.noop),
    ]
