# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-04 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoted', '0019_auto_20161103_1750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ('product', 'quantity')},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('category', 'watt', 'name')},
        ),
        migrations.AddField(
            model_name='orderitem',
            name='price1',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='price2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='price3',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity1',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity2',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity3',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
