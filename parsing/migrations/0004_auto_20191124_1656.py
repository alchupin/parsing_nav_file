# Generated by Django 2.2.7 on 2019-11-24 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0003_auto_20191124_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='navdata',
            name='altitude',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='navdata',
            name='lat_direction',
            field=models.CharField(blank=True, choices=[('N', 'North'), ('E', 'East'), ('S', 'South'), ('W', 'West')], max_length=2),
        ),
        migrations.AddField(
            model_name='navdata',
            name='long_direction',
            field=models.CharField(blank=True, choices=[('N', 'North'), ('E', 'East'), ('S', 'South'), ('W', 'West')], max_length=2),
        ),
        migrations.AddField(
            model_name='navdata',
            name='longitude',
            field=models.CharField(blank=True, max_length=32, verbose_name='Долгота'),
        ),
        migrations.AddField(
            model_name='navdata',
            name='speed',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='navdata',
            name='latitude',
            field=models.CharField(blank=True, max_length=32, verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='navdata',
            name='time_stamp',
            field=models.CharField(blank=True, max_length=32, verbose_name='Время замера'),
        ),
    ]
