# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pfodb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worksheet',
            fields=[
                ('name', models.CharField(primary_key=True, serialize=False, max_length=120)),
                ('updated', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc))),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
