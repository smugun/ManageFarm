# Generated by Django 4.0.4 on 2022-08-27 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mogoon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fertilizer',
            name='fertilizer_labour_rate',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=8),
        ),
        migrations.AddField(
            model_name='fertilizer',
            name='fertilizer_price',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=8),
        ),
    ]
