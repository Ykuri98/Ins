# Generated by Django 2.1.3 on 2018-11-28 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0004_auto_20181128_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='path',
            field=models.TextField(blank=True, max_length=255, null=True, unique=True, verbose_name='path'),
        ),
        migrations.AlterField(
            model_name='login',
            name='userpic',
            field=models.TextField(blank=True, max_length=255, null=True, unique=True, verbose_name='userpic'),
        ),
    ]
