# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pfodb', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Component_or_Item',
        ),
        migrations.CreateModel(
            name='Component_or_Item',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=120)),
                ('plus_value', models.PositiveIntegerField(blank=True)),
                ('tier', models.PositiveIntegerField(choices=[(1, 'I'), (2, 'II'), (3, 'III')], default=1)),
            ],
            options={
                'db_table': 'component_and_item_view',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.RunSQL(
            sql="""
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
    ]
