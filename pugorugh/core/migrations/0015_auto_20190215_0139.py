# Generated by Django 2.1.5 on 2019-02-15 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20190214_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='gender',
            field=models.CharField(blank=True, choices=[('m', 'm'), ('f', 'f')], max_length=10),
        ),
    ]
