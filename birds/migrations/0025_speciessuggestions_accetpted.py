# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-15 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0024_auto_20161229_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='speciessuggestions',
            name='accetpted',
            field=models.BooleanField(default=False),
        ),
    ]
