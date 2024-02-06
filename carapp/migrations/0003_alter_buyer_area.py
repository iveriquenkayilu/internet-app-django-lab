# Generated by Django 5.0.1 on 2024-02-05 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0002_buyer_phone_number_vehicle_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='area',
            field=models.CharField(choices=[('W', 'Windsor'), ('LS', 'LaSalle'), ('A', 'Amherstburg'), ('L', 'Lakeshore'), ('LE', 'Leamington'), ('TO', 'Toronto'), ('CH', 'Chatham'), ('WA', 'Waterloo')], default='CH', max_length=2),
        ),
    ]
