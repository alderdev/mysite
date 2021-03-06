# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-15 08:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.FileField(blank=True, null=True, upload_to='')),
                ('remark', models.CharField(blank=True, max_length=60, null=True)),
                ('timestemp', models.DateTimeField(auto_now_add=True)),
                ('modify', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=30)),
                ('slug', models.SlugField(max_length=30, unique=True)),
            ],
            options={
                'ordering': ('description',),
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=60)),
                ('content', models.TextField()),
                ('timestemp', models.DateTimeField(auto_now_add=True)),
                ('modify', models.DateTimeField(auto_now=True)),
                ('available', models.BooleanField(default=True)),
                ('istop', models.BooleanField(default=False)),
                ('categories', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='posts.Category')),
            ],
            options={
                'ordering': ['-istop', '-modify', 'id'],
            },
        ),
        migrations.AddField(
            model_name='attachment',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Post'),
        ),
    ]
