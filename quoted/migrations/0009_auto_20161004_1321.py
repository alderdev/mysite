# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-04 05:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quoted', '0008_order_ord_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quoted.Order'),
        ),
    ]
