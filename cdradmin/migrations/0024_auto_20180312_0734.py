# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-12 07:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cdradmin', '0023_auto_20180309_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superidtoloanliability',
            name='guarantee_for',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cdradmin.SuperidToLoanLiability'),
        ),
        migrations.AlterField(
            model_name='superidtoloanliability',
            name='ledger',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cdradmin.Ledger'),
        ),
    ]