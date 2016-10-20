# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-20 10:36
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_auto_20161020_1808'),
        ('quoted', '0011_auto_20161020_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='contact',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='customer', chained_model_field='customer', default=1, on_delete=django.db.models.deletion.CASCADE, to='customers.Contact'),
            preserve_default=False,
        ),
    ]