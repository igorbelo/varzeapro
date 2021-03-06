# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-23 21:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20161123_2150'),
    ]

    operations = [
        migrations.CreateModel(
            name='AthleteAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.DateTimeField(blank=True, editable=False, null=True)),
                ('value', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='athlete',
            name='attributes',
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='value',
        ),
        migrations.AddField(
            model_name='athleteattribute',
            name='athlete',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='core.Athlete'),
        ),
        migrations.AddField(
            model_name='athleteattribute',
            name='attribute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Attribute'),
        ),
    ]
