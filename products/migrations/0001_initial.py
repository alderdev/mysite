# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-28 02:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CateDesctiption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=36)),
                ('specification', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to='', width_field='width_field')),
                ('height_field', models.IntegerField(blank=True, default=0, null=True)),
                ('width_field', models.IntegerField(blank=True, default=0, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=36)),
                ('invalid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CycleStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=36)),
                ('invalid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('encoding', models.CharField(max_length=6, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=36)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('part_number', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('specification', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, height_field='height_field', null=True, upload_to='', width_field='width_field')),
                ('height_field', models.IntegerField(blank=True, default=0, null=True)),
                ('width_field', models.IntegerField(blank=True, default=0, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
                ('cycle_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.CycleStatus')),
            ],
        ),
        migrations.AddField(
            model_name='catedesctiption',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category'),
        ),
        migrations.AddField(
            model_name='catedesctiption',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Language'),
        ),
    ]
