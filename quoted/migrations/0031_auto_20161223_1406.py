# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-23 06:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoted', '0030_remove_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='orderitem_modelname',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]
