# Generated by Django 4.2.4 on 2023-08-16 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserva', '0009_delete_aprovador_carro_horaend_carro_horainit_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carro',
            old_name='reserva',
            new_name='dataEnd',
        ),
        migrations.RenameField(
            model_name='sala',
            old_name='reserva',
            new_name='dataEnd',
        ),
        migrations.AddField(
            model_name='carro',
            name='dataInit',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sala',
            name='dataInit',
            field=models.DateField(blank=True, null=True),
        ),
    ]
