# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-02-12 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0030_notifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagePreview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to=b'')),
            ],
        ),
    ]