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
            name='tier',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='crafting_bill_of_materials',
            name='object_id',
            field=models.CharField(max_length=120),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='crafting_recipe',
            name='tier',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='tier',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='tier',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='raw_material',
            name='tier',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='refining_bill_of_materials',
            name='recipe',
            field=models.ForeignKey(to='pfodb.Refining_Recipe', related_name='bill_of_materials'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='refining_recipe',
            name='tier',
            field=models.PositiveIntegerField(default=1),
            preserve_default=True,
        ),
    ]
