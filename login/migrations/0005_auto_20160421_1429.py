# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-21 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20160419_0011'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='type',
        ),
        migrations.AlterField(
            model_name='prof',
            name='type',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
