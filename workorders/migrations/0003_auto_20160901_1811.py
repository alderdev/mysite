# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-01 10:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorders', '0002_workorder_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workorder',
            old_name='reuqest_user',
            new_name='request_user',
        ),
    ]
