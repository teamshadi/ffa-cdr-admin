# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-12 15:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cdradmin', '0030_auto_20180312_1332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country',
            old_name='country',
            new_name='cdr_code',
        ),
    ]
