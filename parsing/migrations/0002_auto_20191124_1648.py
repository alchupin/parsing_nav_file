# Generated by Django 2.2.7 on 2019-11-24 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navdata',
            name='latitude',
            field=models.CharField(max_length=32, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='navdata',
            name='longitude',
            field=models.CharField(max_length=32, verbose_name='Долгота'),
        ),
    ]