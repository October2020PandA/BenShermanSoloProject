# Generated by Django 2.2 on 2020-11-09 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record_app', '0010_auto_20201109_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(),
        ),
    ]
