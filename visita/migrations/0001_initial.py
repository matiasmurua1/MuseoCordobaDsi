# Generated by Django 3.2.4 on 2021-06-20 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empleado', '0003_alter_cargo_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Escuela',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.PositiveSmallIntegerField(choices=[(1, 'Pendiente de confirmacion')], verbose_name='Nombre')),
                ('ambito', models.PositiveSmallIntegerField(choices=[(1, 'Reserva')], verbose_name='Ambito')),
            ],
        ),
        migrations.CreateModel(
            name='ReservaVisita',
            fields=[
                ('cantidadAlumnos', models.PositiveIntegerField(verbose_name='Cantidad de alumnos')),
                ('duracionEstimada', models.PositiveIntegerField(help_text='Duracion expresada en minutos', verbose_name='Duracion estimada')),
                ('fechaHoraCreacion', models.DateTimeField(verbose_name='Fecha y hora de creacion')),
                ('fechaHoraReserva', models.DateTimeField(verbose_name='Fecha y hora de reserva')),
                ('numeroReserva', models.PositiveBigIntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Numero reserva')),
            ],
        ),
        migrations.CreateModel(
            name='TipoVisita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64, verbose_name='Nombre')),
            ],
        ),
        migrations.CreateModel(
            name='CambioEstado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaHoraInicio', models.DateTimeField(verbose_name='Fecha hora de inicio')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='visita.estado')),
            ],
        ),
        migrations.CreateModel(
            name='AsignacionVisita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaHoraFin', models.DateTimeField(verbose_name='Fecha y hora de fin')),
                ('fechaHoraInicio', models.DateTimeField(verbose_name='Fecha y hora de inicio')),
                ('guiaAsignado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='empleado.empleado')),
                ('reservaVisita', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='asignacionGuia', to='visita.reservavisita')),
            ],
        ),
    ]
