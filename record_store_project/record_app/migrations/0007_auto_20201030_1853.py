# Generated by Django 2.2 on 2020-10-30 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record_app', '0006_auto_20201030_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='contents',
            field=models.ManyToManyField(related_name='order', to='record_app.Product'),
        ),
    ]
