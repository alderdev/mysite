# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-13 21:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0004_auto_20160906_1458'),
        ('customers', '0002_auto_20160827_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=36)),
            ],
        ),
        migrations.CreateModel(
            name='QuoteDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_no', models.IntegerField()),
                ('unit_price', models.FloatField()),
                ('line_memo', models.CharField(blank=True, max_length=50, null=True)),
                ('invalid', models.BooleanField(default=False)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.CreateModel(
            name='QuoteHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_user', models.CharField(max_length=60)),
                ('order_number', models.IntegerField(blank=True, null=True, unique=True)),
                ('ord_date', models.DateField(default=django.utils.timezone.now)),
                ('effective_date', models.DateField(default=django.utils.timezone.now)),
                ('invalid', models.BooleanField(default=False)),
                ('comment', models.TextField(blank=True, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('modify', models.DateTimeField(auto_now=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quotations.Currency')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer')),
            ],
        ),
        migrations.AddField(
            model_name='quotedetail',
            name='quotehead',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quotations.QuoteHead'),
        ),
    ]
