# Generated by Django 4.2.4 on 2023-11-16 18:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_usuario_region_id_remove_venta_id_region_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuario',
            old_name='rol_id',
            new_name='rol',
        ),
    ]