# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-27 09:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='contect',
            new_name='contact',
        ),
    ]
