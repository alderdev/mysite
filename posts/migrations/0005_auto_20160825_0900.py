# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-25 01:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20160825_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to='', width_field='width_field'),
        ),
    ]
