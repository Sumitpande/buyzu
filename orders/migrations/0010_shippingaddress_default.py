# Generated by Django 3.1.4 on 2021-05-29 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20210528_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
