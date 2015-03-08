# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crafting_Bill_Of_Materials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('object_id', models.CharField(max_length=120)),
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
                ('name', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('tier', models.PositiveIntegerField(default=1)),
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
            name='Equipment',
            fields=[
                ('name', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('tier', models.PositiveIntegerField(default=1)),
                ('category', models.CharField(max_length=120)),
                ('quality', models.PositiveIntegerField()),
                ('recipe', models.OneToOneField(to='pfodb.Crafting_Recipe', related_name='output')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('rank', models.PositiveIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Raw_Ingredient',
            fields=[
                ('name', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('tier', models.PositiveIntegerField(default=1)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Raw_Material',
            fields=[
                ('name', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('tier', models.PositiveIntegerField(default=1)),
                ('ingredients', models.ManyToManyField(to='pfodb.Raw_Ingredient', related_name='sources')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Refined_Ingredient',
            fields=[
                ('name', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('tier', models.PositiveIntegerField(default=1)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Refined_Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('plus_value', models.PositiveIntegerField(default=0)),
                ('tier', models.PositiveIntegerField(default=1)),
                ('variety', models.CharField(max_length=120)),
                ('quality', models.PositiveIntegerField()),
                ('ingredient', models.ForeignKey(to='pfodb.Refined_Ingredient', related_name='sources')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Refining_Bill_Of_Materials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField()),
                ('material', models.ForeignKey(to='pfodb.Raw_Ingredient', related_name='used_by')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Refining_Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('plus_value', models.PositiveIntegerField(default=0)),
                ('tier', models.PositiveIntegerField(default=1)),
                ('output_quantity', models.PositiveIntegerField()),
                ('base_crafting_seconds', models.PositiveIntegerField()),
                ('achievement_type', models.CharField(max_length=120)),
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
            field=models.ForeignKey(related_query_name='material', to='pfodb.Refining_Recipe', related_name='materials'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='refining_bill_of_materials',
            unique_together=set([('recipe', 'material')]),
        ),
        migrations.AddField(
            model_name='refined_material',
            name='recipe',
            field=models.OneToOneField(to='pfodb.Refining_Recipe', related_name='output'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='refined_material',
            unique_together=set([('name', 'plus_value')]),
        ),
        migrations.AlterIndexTogether(
            name='refined_material',
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
            field=models.ForeignKey(related_query_name='material', to='pfodb.Crafting_Recipe', related_name='materials'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='crafting_bill_of_materials',
            unique_together=set([('recipe', 'object_id', 'content_type')]),
        ),
    ]
