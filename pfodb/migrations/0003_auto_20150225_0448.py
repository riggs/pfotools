# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pfodb', '0002_auto_20150225_0205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='raw_material',
            name='elements',
        ),
        migrations.AddField(
            model_name='raw_material',
            name='ingredients',
            field=models.ManyToManyField(related_name='sources', to='pfodb.Ingredient'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='crafting_bill_of_materials',
            name='recipe',
            field=models.ForeignKey(related_name='bill_of_materials', to='pfodb.Crafting_Recipe'),
            preserve_default=True,
        ),
    ]
