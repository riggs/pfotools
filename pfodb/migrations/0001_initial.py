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
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=120)),
                ('plus_value', models.PositiveIntegerField(default=0)),
                ('tier', models.PositiveIntegerField(default=1, choices=[(1, 'I'), (2, 'II'), (3, 'III')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Component_Material',
            fields=[
                ('name', models.CharField(serialize=False, primary_key=True, max_length=120)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Crafting_Measure',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('object_id', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Crafting_Recipe',
            fields=[
                ('name', models.CharField(serialize=False, primary_key=True, max_length=120)),
                ('tier', models.PositiveIntegerField(default=1, choices=[(1, 'I'), (2, 'II'), (3, 'III')])),
                ('required_feat_rank', models.PositiveIntegerField(default=0)),
                ('output_quantity', models.PositiveIntegerField(default=1)),
                ('base_crafting_seconds', models.PositiveIntegerField()),
                ('quality', models.PositiveIntegerField()),
                ('category', models.CharField(max_length=120)),
                ('achievement_type', models.CharField(max_length=120)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('name', models.CharField(serialize=False, primary_key=True, max_length=120)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feat',
            fields=[
                ('name', models.CharField(serialize=False, primary_key=True, max_length=120)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=120)),
                ('plus_value', models.PositiveIntegerField(default=0)),
                ('tier', models.PositiveIntegerField(default=1, choices=[(1, 'I'), (2, 'II'), (3, 'III')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item_Type',
            fields=[
                ('name', models.CharField(serialize=False, primary_key=True, max_length=120)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Raw_Material',
            fields=[
                ('name', models.CharField(serialize=False, primary_key=True, max_length=120)),
                ('elements', models.ManyToManyField(related_name='sources', related_query_name='source', to='pfodb.Element')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Refining_Measure',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('material', models.ForeignKey(related_name='measures', to='pfodb.Element', related_query_name='measure')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Refining_Recipe',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=120)),
                ('plus_value', models.PositiveIntegerField(default=0)),
                ('tier', models.PositiveIntegerField(default=1, choices=[(1, 'I'), (2, 'II'), (3, 'III')])),
                ('required_feat_rank', models.PositiveIntegerField(default=0)),
                ('output_quantity', models.PositiveIntegerField(default=1)),
                ('base_crafting_seconds', models.PositiveIntegerField()),
                ('quality', models.PositiveIntegerField()),
                ('category', models.CharField(max_length=120)),
                ('achievement_type', models.CharField(max_length=120)),
                ('ingredients', models.ManyToManyField(related_name='used_by', to='pfodb.Element', through='pfodb.Refining_Measure')),
                ('output', models.OneToOneField(related_name='recipes', to='pfodb.Component', related_query_name='recipe')),
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
            model_name='refining_measure',
            name='recipe',
            field=models.ForeignKey(related_name='elements', to='pfodb.Refining_Recipe', related_query_name='element'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.ForeignKey(to='pfodb.Item_Type'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('name', 'plus_value')]),
        ),
        migrations.AlterIndexTogether(
            name='item',
            index_together=set([('name', 'plus_value')]),
        ),
        migrations.AddField(
            model_name='crafting_recipe',
            name='output',
            field=models.OneToOneField(related_name='recipes', to='pfodb.Item', related_query_name='recipe'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crafting_recipe',
            name='required_feat',
            field=models.ForeignKey(to='pfodb.Feat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crafting_measure',
            name='recipe',
            field=models.ForeignKey(related_name='elements', to='pfodb.Crafting_Recipe', related_query_name='element'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='component',
            name='material',
            field=models.ForeignKey(to='pfodb.Component_Material'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='component',
            unique_together=set([('name', 'plus_value')]),
        ),
        migrations.AlterIndexTogether(
            name='component',
            index_together=set([('name', 'plus_value')]),
        ),
    ]
