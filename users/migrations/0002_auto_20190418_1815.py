# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-18 18:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='zipcode',
            new_name='zip',
        ),
    ]
