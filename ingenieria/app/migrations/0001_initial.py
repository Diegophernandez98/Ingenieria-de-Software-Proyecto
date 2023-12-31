# Generated by Django 4.2.6 on 2023-11-19 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dudas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo', models.CharField(max_length=50)),
                ('duda', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.IntegerField(default=10000)),
                ('stock', models.IntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='Rol_Lista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('rut', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('correo', models.CharField(max_length=50)),
                ('celular', models.CharField(max_length=50)),
                ('comuna', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('contrasena', models.CharField(max_length=50)),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.rol_lista')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField()),
                ('fecha', models.DateTimeField()),
                ('comuna', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.producto')),
                ('id_tipo_animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tipo_animal')),
                ('id_tipo_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tipo_producto')),
                ('rut_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='id_tipo_animal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tipo_animal'),
        ),
        migrations.AddField(
            model_name='producto',
            name='id_tipo_producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.tipo_producto'),
        ),
    ]
