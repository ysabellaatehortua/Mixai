# Generated by Django 4.0 on 2022-01-23 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_chromosomedb_rating_population_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='population',
            name='training',
        ),
    ]
