# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-29 17:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('birds', '0014_speciessuggestions'),
    ]

    operations = [
        migrations.CreateModel(
            name='BirdPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=b'')),
            ],
        ),
        migrations.RemoveField(
            model_name='sighting',
            name='image',
        ),
        migrations.AddField(
            model_name='birdphoto',
            name='sighting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='birds.Sighting'),
        ),
    ]