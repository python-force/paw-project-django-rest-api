# Generated by Django 2.1.2 on 2019-02-08 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190208_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='image_filename',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]