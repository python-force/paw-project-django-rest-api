# Generated by Django 2.1.5 on 2019-02-09 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20190208_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdog',
            name='status',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]
