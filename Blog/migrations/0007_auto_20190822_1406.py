# Generated by Django 2.0 on 2019-08-22 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0006_auto_20190820_1237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readnum',
            name='blog',
        ),
        migrations.DeleteModel(
            name='ReadNum',
        ),
    ]
