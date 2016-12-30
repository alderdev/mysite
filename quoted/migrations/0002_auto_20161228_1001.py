# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-28 02:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quoted', '0001_initial'),
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
            name='DimmingOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('quote_sales', models.CharField(blank=True, max_length=60, null=True)),
                ('ord_date', models.DateField(default=django.utils.timezone.now)),
                ('effective_date', models.DateField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('paid', models.BooleanField(default=False)),
                ('order_number', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('contact', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='customer', chained_model_field='customer', on_delete=django.db.models.deletion.CASCADE, to='customers.Contact')),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quoted.Currency')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.Customer')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_special', models.BooleanField(default=False, verbose_name='Customized Product')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price1', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('quantity1', models.PositiveIntegerField(blank=True, null=True)),
                ('price2', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('quantity2', models.PositiveIntegerField(blank=True, null=True)),
                ('price3', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('quantity3', models.PositiveIntegerField(blank=True, null=True)),
                ('line_remark', models.CharField(blank=True, max_length=60, null=True, verbose_name='Remark')),
                ('orderitem_name', models.CharField(max_length=60, verbose_name='Product Name')),
                ('orderitem_modelname', models.CharField(max_length=60, verbose_name='Model Name')),
                ('orderitem_option1', models.CharField(max_length=60, verbose_name='Option')),
                ('orderitem_beam_angle', models.CharField(max_length=60, verbose_name='Beam angle')),
                ('orderitem_cct', models.CharField(max_length=60, verbose_name='CCT')),
                ('orderitem_cri', models.CharField(max_length=60, verbose_name='CRI')),
                ('orderitem_watt', models.CharField(max_length=60, verbose_name='WATT')),
                ('orderitem_lm', models.CharField(max_length=60, verbose_name='LM')),
                ('orderitem_image', models.ImageField(blank=True, height_field='orderitem_height_field', null=True, upload_to='', verbose_name='Image', width_field='orderitem_width_field')),
                ('orderitem_height_field', models.IntegerField(blank=True, default=0, null=True)),
                ('orderitem_width_field', models.IntegerField(blank=True, default=0, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quoted.Order')),
                ('orderitem_dimming', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quoted.DimmingOption', verbose_name='Dimming')),
            ],
            options={
                'ordering': ('product',),
            },
        ),
        migrations.CreateModel(
            name='PaymentTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PriceTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('std_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('min_sell', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quoted.Currency')),
            ],
            options={
                'ordering': ['-currency'],
            },
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('category', 'watt', 'name')},
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.AlterField(
            model_name='product',
            name='cct',
            field=models.CharField(max_length=60, verbose_name='CCT'),
        ),
        migrations.AlterField(
            model_name='product',
            name='cri',
            field=models.CharField(max_length=60, verbose_name='CRI'),
        ),
        migrations.AlterField(
            model_name='product',
            name='modelname',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='productprice',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quoted.Product'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='quoted.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='paymentterm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quoted.PaymentTerm'),
        ),
        migrations.AddField(
            model_name='order',
            name='priceterm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quoted.PriceTerm'),
        ),
        migrations.AddField(
            model_name='order',
            name='quote_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='dimming',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quoted.DimmingOption'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='productprice',
            unique_together=set([('product', 'currency')]),
        ),
    ]
