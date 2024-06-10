# Generated by Django 4.2.4 on 2024-06-10 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserva', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('approver', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('hours_registred', models.JSONField(null=True)),
            ],
        ),
    ]
