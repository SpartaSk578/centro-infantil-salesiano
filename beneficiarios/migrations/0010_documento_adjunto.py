from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiarios', '0009_preinscripcion_anio_semestre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiario',
            name='documento_adjunto',
            field=models.FileField(blank=True, null=True, upload_to='beneficiarios/documentos/'),
        ),
        migrations.AddField(
            model_name='tutorpadre',
            name='documento_adjunto',
            field=models.FileField(blank=True, null=True, upload_to='tutores/documentos/'),
        ),
    ]