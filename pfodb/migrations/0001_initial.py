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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
            name='Crafted_Item_Measure',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
                ('tier', models.PositiveIntegerField(choices=[(1, 'I'), (2, 'II'), (3, 'III')], default=1)),
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
            name='Element_Measure',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('material', models.ForeignKey(related_query_name='measure', to='pfodb.Element', related_name='measures')),
            ],
            options={
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
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
            name='Raw_Material',
            fields=[
                ('name', models.CharField(serialize=False, primary_key=True, max_length=120)),
                ('elements', models.ManyToManyField(to='pfodb.Element', related_name='sources', related_query_name='source')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Refining_Recipe',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('plus_value', models.PositiveIntegerField(blank=True)),
                ('tier', models.PositiveIntegerField(choices=[(1, 'I'), (2, 'II'), (3, 'III')], default=1)),
                ('required_feat_rank', models.PositiveIntegerField(default=0)),
                ('output_quantity', models.PositiveIntegerField(default=1)),
                ('base_crafting_seconds', models.PositiveIntegerField()),
                ('quality', models.PositiveIntegerField()),
                ('category', models.CharField(max_length=120)),
                ('achievement_type', models.CharField(max_length=120)),
                ('ingredients', models.ManyToManyField(to='pfodb.Element', through='pfodb.Element_Measure', related_name='used_by')),
                ('output', models.OneToOneField(related_query_name='recipe', to='pfodb.Component', related_name='recipes')),
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
            field=models.ForeignKey(related_query_name='element', to='pfodb.Refining_Recipe', related_name='elements'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crafting_recipe',
            name='output',
            field=models.OneToOneField(related_query_name='recipe', to='pfodb.Item', related_name='recipes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crafting_recipe',
            name='required_feat',
            field=models.ForeignKey(to='pfodb.Feat'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crafted_item_measure',
            name='recipe',
            field=models.ForeignKey(related_query_name='element', to='pfodb.Crafting_Recipe', related_name='elements'),
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
