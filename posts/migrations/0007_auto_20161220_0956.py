# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-20 01:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20160825_1312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['ontop', 'modify', 'id']},
        ),
        migrations.AddField(
            model_name='post',
            name='ontop',
            field=models.BooleanField(default=False),
        ),
    ]
