# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-22 01:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hits', '0002_auto_20180921_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='hittemplate',
            name='login_required',
            field=models.BooleanField(default=True),
        ),
    ]