# Generated by Django 2.1.3 on 2018-11-28 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.TextField(max_length=255, unique=True, verbose_name='path')),
                ('description', models.TextField(max_length=610, verbose_name='des')),
                ('like', models.IntegerField()),
                ('createTime', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='login',
            name='path',
            field=models.TextField(blank=True, max_length=255, unique=True, verbose_name='path'),
        ),
        migrations.AddField(
            model_name='login',
            name='userpic',
            field=models.TextField(blank=True, max_length=255, unique=True, verbose_name='userpic'),
        ),
    ]