# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-03 08:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quoted', '0015_dimmingoption'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='dimming',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quoted.DimmingOption'),
        ),
    ]