# Generated by Django 2.0.7 on 2018-11-28 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0005_auto_20181128_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='path',
            field=models.TextField(max_length=255, verbose_name='path'),
        ),
    ]