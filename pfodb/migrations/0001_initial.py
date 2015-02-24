# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=120)),
                ('plus_value', models.PositiveIntegerField(default=0)),
                ('tier', models.PositiveIntegerField(default=1, choices=[(1, 'I'), (2, 'II'), (3, 'III')])),
                ('variety', models.CharField(max_length=120)),
                ('quality', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Crafting_Bill_Of_Materials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Crafting_Recipe',
            fields=[
                ('name', models.CharField(max_length=120, serialize=False, primary_key=True)),
                ('tier', models.PositiveIntegerField(default=1, choices=[(1, 'I'), (2, 'II'), (3, 'III')])),
                ('output_quantity', models.PositiveIntegerField()),
                ('base_crafting_seconds', models.PositiveIntegerField()),
                ('achievement_type', models.CharField(max_length=120)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=120)),
                ('rank', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('name', models.CharField(max_length=120, serialize=False, primary_key=True)),
                ('tier', models.PositiveIntegerField(default=1, choices=[(1, 'I'), (2, 'II'), (3, 'III')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=120)),
                ('plus_value', models.PositiveIntegerField(default=0)),
                ('tier', models.PositiveIntegerField(default=1, choices=[(1, 'I'), (2, 'II'), (3, 'III')])),
                ('category', models.CharField(max_length=120)),
                ('quality', models.PositiveIntegerField()),
                ('recipe', models.ForeignKey(to='pfodb.Crafting_Recipe', related_query_name='output', related_name='outputs')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Raw_Material',
            fields=[
                ('name', models.CharField(max_length=120, serialize=False, primary_key=True)),
                ('tier', models.PositiveIntegerField(default=1, choices=[(1, 'I'), (2, 'II'), (3, 'III')])),
                ('elements', models.ManyToManyField(to='pfodb.Ingredient')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Refining_Bill_Of_Materials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('quantity', models.PositiveIntegerField()),
                ('material', models.ForeignKey(to='pfodb.Ingredient', related_query_name='component', related_name='components')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Refining_Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=120)),
                ('plus_value', models.PositiveIntegerField(default=0)),
                ('tier', models.PositiveIntegerField(default=1, choices=[(1, 'I'), (2, 'II'), (3, 'III')])),
                ('output_quantity', models.PositiveIntegerField()),
                ('base_crafting_seconds', models.PositiveIntegerField()),
                ('achievement_type', models.CharField(max_length=120)),
                ('ingredients', models.ManyToManyField(to='pfodb.Ingredient', related_name='used_by', through='pfodb.Refining_Bill_Of_Materials')),
                ('required_feat', models.ForeignKey(to='pfodb.Feat')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='refining_recipe',
            unique_together=set([('name', 'plus_value')]),
        ),
        migrations.AlterIndexTogether(
            name='refining_recipe',
            index_together=set([('name', 'plus_value')]),
        ),
        migrations.AddField(
            model_name='refining_bill_of_materials',
            name='recipe',
            field=models.ForeignKey(to='pfodb.Refining_Recipe', related_query_name='element', related_name='elements'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='refining_bill_of_materials',
            unique_together=set([('recipe', 'material')]),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('name', 'plus_value')]),
        ),
        migrations.AlterIndexTogether(
            name='item',
            index_together=set([('name', 'plus_value')]),
        ),
        migrations.AlterUniqueTogether(
            name='feat',
            unique_together=set([('name', 'rank')]),
        ),
        migrations.AlterIndexTogether(
            name='feat',
            index_together=set([('name', 'rank')]),
        ),
        migrations.AddField(
            model_name='crafting_recipe',
            name='required_feat',
            field=models.ForeignKey(to='pfodb.Feat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crafting_bill_of_materials',
            name='recipe',
            field=models.ForeignKey(to='pfodb.Crafting_Recipe', related_query_name='ingredient', related_name='ingredients'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='crafting_bill_of_materials',
            unique_together=set([('recipe', 'object_id')]),
        ),
        migrations.AddField(
            model_name='component',
            name='recipe',
            field=models.OneToOneField(to='pfodb.Refining_Recipe', related_name='output'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='component',
            unique_together=set([('name', 'plus_value', 'recipe')]),
        ),
        migrations.AlterIndexTogether(
            name='component',
            index_together=set([('name', 'plus_value')]),
        ),
    ]
