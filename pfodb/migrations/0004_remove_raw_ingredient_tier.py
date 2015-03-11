# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pfodb', '0003_auto_20150311_0657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='raw_ingredient',
            name='tier',
        ),
    ]
