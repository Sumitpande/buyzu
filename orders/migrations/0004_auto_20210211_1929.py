# Generated by Django 3.1.4 on 2021-02-11 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20210113_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='mobile',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(blank=True, choices=[('MH', 'Maharashtra'), ('Goa', 'Goa'), ('UP', 'Uttar Pradesh'), ('MP', 'Madhya Pradesh')], max_length=250, null=True),
        ),
    ]
