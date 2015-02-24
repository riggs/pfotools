# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pfodb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='plus_value',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='plus_value',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='refining_recipe',
            name='plus_value',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
