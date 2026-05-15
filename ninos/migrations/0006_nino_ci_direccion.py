from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ninos', '0005_documentonino'),
    ]

    operations = [
        migrations.AddField(
            model_name='nino',
            name='ci_nino',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='CI del Niño/a'),
        ),
        migrations.AddField(
            model_name='nino',
            name='direccion',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Dirección'),
        ),
    ]
