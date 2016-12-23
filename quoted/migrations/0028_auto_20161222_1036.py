# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-22 02:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quoted', '0027_auto_20161216_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='orderitem_beam_angle',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orderitem_cct',
            field=models.CharField(default=1, max_length=60, verbose_name='CCT'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orderitem_cri',
            field=models.CharField(default=1, max_length=60, verbose_name='CRI'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orderitem_dimming',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quoted.DimmingOption'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orderitem_height_field',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orderitem_image',
            field=models.ImageField(blank=True, height_field='orderitem_height_field', null=True, upload_to='', width_field='orderitem_width_field'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orderitem_lm',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orderitem_modelname',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orderitem_name',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orderitem_option1',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orderitem_watt',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='orderitem_width_field',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
