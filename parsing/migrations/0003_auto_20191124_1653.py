# Generated by Django 2.2.7 on 2019-11-24 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0002_auto_20191124_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='navdata',
            name='altitude',
        ),
        migrations.RemoveField(
            model_name='navdata',
            name='lat_direction',
        ),
        migrations.RemoveField(
            model_name='navdata',
            name='long_direction',
        ),
        migrations.RemoveField(
            model_name='navdata',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='navdata',
            name='speed',
        ),
    ]
