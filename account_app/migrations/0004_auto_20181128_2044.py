# Generated by Django 2.1.3 on 2018-11-28 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0003_auto_20181128_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='path',
            field=models.TextField(blank=True, max_length=255, unique=True, verbose_name='path'),
        ),
    ]