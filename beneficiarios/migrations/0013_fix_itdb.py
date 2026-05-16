from django.db import migrations

def fix_itdb(apps, schema_editor):
    Beneficiario = apps.get_model('beneficiarios', 'Beneficiario')
    # Por si quedaron registros con IDTB en BD, corregirlos a ITDB
    Beneficiario.objects.filter(ocupacion='ESTUDIANTE_IDTB').update(ocupacion='ESTUDIANTE_ITDB')

class Migration(migrations.Migration):
    dependencies = [
        ('beneficiarios', '0012_rename_itdb_to_idtb'),
    ]
    operations = [
        migrations.RunPython(fix_itdb, migrations.RunPython.noop),
    ]
