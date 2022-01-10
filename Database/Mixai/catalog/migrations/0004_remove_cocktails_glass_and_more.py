# Generated by Django 4.0 on 2022-01-06 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_cocktails_alcoholic_cocktails_glass'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cocktails',
            name='glass',
        ),
        migrations.RemoveField(
            model_name='ingredients',
            name='ingredient_description',
        ),
        migrations.RemoveField(
            model_name='measurements',
            name='measurement_name',
        ),
        migrations.RemoveField(
            model_name='measurements',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='recipesteps',
            name='step_description',
        ),
        migrations.RemoveField(
            model_name='recipesteps',
            name='step_number',
        ),
        migrations.RemoveField(
            model_name='recipesteps',
            name='tool',
        ),
        migrations.AddField(
            model_name='ingredients',
            name='ingredient_type',
            field=models.CharField(choices=[('alcohol', 'Alcohol'), ('mixer', 'Mixer'), ('modifier', 'Modifier'), ('liqueur', 'Liqueur')], default='mixer', max_length=10),
        ),
        migrations.DeleteModel(
            name='Tools',
        ),
    ]
