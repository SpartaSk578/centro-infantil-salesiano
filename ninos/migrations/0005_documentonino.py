from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ninos', '0004_nino_nuevos_campos'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentoNino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del documento')),
                ('archivo', models.FileField(upload_to='ninos/documentos/')),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
                ('nino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='ninos.nino')),
            ],
            options={'verbose_name': 'Documento', 'verbose_name_plural': 'Documentos'},
        ),
    ]
