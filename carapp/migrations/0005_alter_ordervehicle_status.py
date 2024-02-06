# Generated by Django 5.0.1 on 2024-02-05 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0004_ordervehicle_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordervehicle',
            name='status',
            field=models.IntegerField(choices=[(0, 'cancelled'), (1, 'placed'), (2, 'shipped'), (3, 'delivered'), (4, 'successful')], default=1),
        ),
    ]
