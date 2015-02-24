# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pfodb', '0002_auto_20150224_0255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component_Material',
            fields=[
                ('name', models.CharField(max_length=120, serialize=False, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item_Type',
            fields=[
                ('name', models.CharField(max_length=120, serialize=False, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='component',
            name='material',
            field=models.ForeignKey(default=datetime.datetime(2015, 2, 24, 4, 10, 33, 653626, tzinfo=utc), to='pfodb.Component_Material'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='type',
            field=models.ForeignKey(default=datetime.datetime(2015, 2, 24, 4, 10, 48, 661418, tzinfo=utc), to='pfodb.Item_Type'),
            preserve_default=False,
        ),
    ]
