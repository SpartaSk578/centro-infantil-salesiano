from django.db import migrations


def rename_itdb_to_idtb(apps, schema_editor):
    Beneficiario = apps.get_model('beneficiarios', 'Beneficiario')
    Beneficiario.objects.filter(ocupacion='ESTUDIANTE_ITDB').update(ocupacion='ESTUDIANTE_IDTB')


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiarios', '0011_alter_beneficiario_ocupacion_and_more'),
    ]

    operations = [
        migrations.RunPython(rename_itdb_to_idtb, migrations.RunPython.noop),
    ]
