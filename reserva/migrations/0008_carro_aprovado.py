# Generated by Django 4.2.4 on 2023-08-09 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserva', '0007_sala_aprovado'),
    ]

    operations = [
        migrations.AddField(
            model_name='carro',
            name='aprovado',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
