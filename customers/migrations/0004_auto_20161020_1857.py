# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-20 10:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20161020_1808'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['-master']},
        ),
    ]