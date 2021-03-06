# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-28 02:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialCtrlOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=36)),
                ('invalid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OrderCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=36)),
                ('order_squence', models.IntegerField(default=1000)),
                ('invalid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recevice_date', models.DateField(default=django.utils.timezone.now)),
                ('ships_order', models.CharField(blank=True, max_length=16, null=True)),
                ('work_order', models.CharField(max_length=16, unique=True)),
                ('ord_amount', models.IntegerField(default=1)),
                ('deliverly', models.DateField(blank=True, null=True)),
                ('material_ready_date', models.DateField(blank=True, null=True)),
                ('estimated_finish', models.DateField(blank=True, null=True)),
                ('request_user', models.CharField(max_length=16)),
                ('material_duty', models.CharField(max_length=16)),
                ('manage_memo', models.TextField(blank=True, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify', models.DateTimeField(auto_now=True)),
                ('last_access', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workorders.OrderCategory')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer')),
                ('material_ctrl', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workorders.MaterialCtrlOption')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
            options={
                'ordering': ['-last_access'],
            },
        ),
        migrations.CreateModel(
            name='ZmmsOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=36)),
                ('invalid', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='workorder',
            name='zmms',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workorders.ZmmsOption'),
        ),
    ]
