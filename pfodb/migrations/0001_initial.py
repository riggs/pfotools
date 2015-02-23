# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('plus_value', models.PositiveIntegerField(blank=True)),
                ('tier', models.PositiveIntegerField(choices=[(1, 'I'), (2, 'II'), (3, 'III')], default=1)),
                ],
            options={
                'abstract': False,
                },
            bases=(models.Model,),
            ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('plus_value', models.PositiveIntegerField(blank=True)),
                ('tier', models.PositiveIntegerField(choices=[(1, 'I'), (2, 'II'), (3, 'III')], default=1)),
                ],
            options={
                'abstract': False,
                },
            bases=(models.Model,),
            ),
        migrations.RunSQL(
            sql="""
                DROP TABLE IF EXISTS "component_and_item_view" CASCADE ;
                CREATE VIEW "component_and_item_view" AS
                  SELECT id = row_number() OVER (ORDER BY "tier" ASC, "name" ASC, "plus_value" ASC),
                         "name", "plus_value", "tier"
                    FROM
                    (
                      SELECT "name", "plus_value", "tier" FROM pfodb_component
                        UNION
                      SELECT "name", "plus_value", "tier" FROM pfodb_item ORDER BY tier
                    ) AS _;
                """
        ),
        migrations.CreateModel(
            name='Component_or_Item_Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('material', models.ForeignKey(related_name='measures', related_query_name='measure', to='pfodb.Component_or_Item')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Crafting_Recipe',
            fields=[
                ('name', models.CharField(serialize=False, primary_key=True, max_length=120)),
                ('tier', models.PositiveIntegerField(choices=[(1, 'I'), (2, 'II'), (3, 'III')], default=1)),
                ('required_feat_rank', models.PositiveIntegerField(default=0)),
                ('output_quantity', models.PositiveIntegerField(default=1)),
                ('base_crafting_seconds', models.PositiveIntegerField()),
                ('quality', models.PositiveIntegerField()),
                ('category', models.CharField(max_length=120)),
                ('achievement_type', models.CharField(max_length=120)),
                ('ingredients', models.ManyToManyField(related_name='uses', through='pfodb.Component_or_Item_Measure', related_query_name='usage', to='pfodb.Component_or_Item')),
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
            name='Element_Measure',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('material', models.ForeignKey(related_name='measures', related_query_name='measure', to='pfodb.Element')),
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
            name='Refining_Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('plus_value', models.PositiveIntegerField(blank=True)),
                ('tier', models.PositiveIntegerField(choices=[(1, 'I'), (2, 'II'), (3, 'III')], default=1)),
                ('required_feat_rank', models.PositiveIntegerField(default=0)),
                ('output_quantity', models.PositiveIntegerField(default=1)),
                ('base_crafting_seconds', models.PositiveIntegerField()),
                ('quality', models.PositiveIntegerField()),
                ('category', models.CharField(max_length=120)),
                ('achievement_type', models.CharField(max_length=120)),
                ('ingredients', models.ManyToManyField(related_name='uses', through='pfodb.Element_Measure', related_query_name='usage', to='pfodb.Element')),
                ('output', models.OneToOneField(related_name='Component_recipe', to='pfodb.Component')),
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
        migrations.AlterUniqueTogether(
            name='item',
            unique_together=set([('name', 'plus_value')]),
        ),
        migrations.AlterIndexTogether(
            name='item',
            index_together=set([('name', 'plus_value')]),
        ),
        migrations.AddField(
            model_name='element_measure',
            name='recipe',
            field=models.ForeignKey(related_name='Elements', related_query_name='Element', to='pfodb.Refining_Recipe'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crafting_recipe',
            name='output',
            field=models.OneToOneField(related_name='Item_recipe', to='pfodb.Item'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crafting_recipe',
            name='required_feat',
            field=models.ForeignKey(to='pfodb.Feat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='component_or_item_measure',
            name='recipe',
            field=models.ForeignKey(related_name='Component_or_Items', related_query_name='Component_or_Item', to='pfodb.Crafting_Recipe'),
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
