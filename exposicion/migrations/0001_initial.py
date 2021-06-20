# Generated by Django 3.2.4 on 2021-06-20 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duracionExtendida', models.PositiveIntegerField(verbose_name='Duracion extendida')),
            ],
        ),
        migrations.CreateModel(
            name='PublicoDestino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Sede',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantMaximaVisita', models.PositiveIntegerField(verbose_name='Cantidad maxima de visitantes')),
                ('cantMaximaPorGuia', models.PositiveIntegerField(verbose_name='Cantidad maxima por guia')),
                ('nombre', models.CharField(max_length=64, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='TipoExposicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('Tem', 'Temporal')], max_length=3, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Exposicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaFin', models.DateField(verbose_name='Fecha fin')),
                ('fechaInicio', models.DateField(verbose_name='Fecha inicio')),
                ('fechaFinReplanificada', models.DateField(null=True, verbose_name='Fecha fin replanificada')),
                ('fechaInicioReplanificada', models.DateField(null=True, verbose_name='Fecha inicio replanificada')),
                ('horaApertura', models.TimeField(verbose_name='Hora apertura')),
                ('horaCierre', models.TimeField(verbose_name='Hora cierre')),
                ('nombre', models.CharField(max_length=64, verbose_name='Nombre')),
                ('publicoDestino', models.ManyToManyField(to='exposicion.PublicoDestino')),
                ('tipoExposicion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exposicion.tipoexposicion')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleExposicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exposicion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exposicion.exposicion')),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exposicion.obra')),
            ],
        ),
    ]
