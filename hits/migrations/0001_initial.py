# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-23 20:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('input_csv_fields', jsonfield.fields.JSONField()),
                ('answers', jsonfield.fields.JSONField(blank=True)),
            ],
            options={
                'verbose_name': 'HIT',
            },
        ),
        migrations.CreateModel(
            name='HitBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('filename', models.CharField(max_length=1024)),
                ('name', models.CharField(max_length=1024)),
            ],
            options={
                'verbose_name': 'HIT batch',
                'verbose_name_plural': 'HIT batches',
            },
        ),
        migrations.CreateModel(
            name='HitTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=1024)),
                ('name', models.CharField(max_length=1024)),
                ('form', models.TextField()),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'HIT template',
            },
        ),
        migrations.AddField(
            model_name='hitbatch',
            name='hit_template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hits.HitTemplate'),
        ),
        migrations.AddField(
            model_name='hit',
            name='hit_batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hits.HitBatch'),
        ),
    ]
