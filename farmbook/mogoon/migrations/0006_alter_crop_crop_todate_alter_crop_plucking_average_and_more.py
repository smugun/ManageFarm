# Generated by Django 4.0.4 on 2022-08-12 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mogoon', '0005_alter_crop_crop_todate_alter_crop_plucking_average_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop',
            name='crop_todate',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='crop',
            name='plucking_average',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='crop',
            name='total_crop',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]