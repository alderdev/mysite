# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-26 06:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0003_auto_20160926_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotedetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prod_model.ProdModel'),
        ),
    ]