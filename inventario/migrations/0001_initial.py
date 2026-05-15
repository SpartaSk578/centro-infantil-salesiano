from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('grupos', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemInventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre del recurso')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('estado', models.CharField(
                    choices=[('ALTA', 'Alta (Buen estado)'), ('REGULAR', 'Regular'), ('BAJA', 'Baja (Dañado/Perdido)')],
                    default='ALTA', max_length=10)),
                ('tipo_movimiento', models.CharField(
                    choices=[('DONACION', 'Donación'), ('COMPRA', 'Compra'), ('ROTURA', 'Rotura'), ('PERDIDA', 'Pérdida'), ('OTRO', 'Otro')],
                    default='DONACION', max_length=15)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('foto1', models.ImageField(blank=True, null=True, upload_to='inventario/')),
                ('foto2', models.ImageField(blank=True, null=True, upload_to='inventario/')),
                ('foto3', models.ImageField(blank=True, null=True, upload_to='inventario/')),
                ('grupo', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='inventario', to='grupos.grupo')),
                ('registrado_por', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Ítem de Inventario',
                'verbose_name_plural': 'Inventario',
                'ordering': ['grupo', 'nombre'],
            },
        ),
    ]
