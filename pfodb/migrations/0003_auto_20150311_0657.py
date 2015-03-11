# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pfodb', '0002_worksheet'),
    ]

    operations = [
        migrations.AddField(
            model_name='raw_material',
            name='encumbrance',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='raw_material',
            name='variety',
            field=models.CharField(default='', max_length=120),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='refining_bill_of_materials',
            name='material',
            field=models.ForeignKey(to='pfodb.Raw_Ingredient', related_name='ingredient_of'),
            preserve_default=True,
        ),
    ]
