# Generated by Django 4.0.4 on 2022-05-18 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gasolinapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gasolinera',
            name='location',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='gasolinera',
            name='schedule',
            field=models.CharField(max_length=100),
        ),
    ]
