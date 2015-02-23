# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pfodb', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(sql="""
                            CREATE VIEW "component_and_item_view" AS
                              SELECT id = row_number() OVER (ORDER BY "tier" ASC, "name" ASC, "plus_value" ASC),
                                      "name", "plus_value", "tier"
                                FROM
                                (
                                  SELECT "name", "plus_value", "tier" FROM pfodb_component
                                    UNION
                                  SELECT "name", "plus_value", "tier" FROM pfodb_item ORDER BY tier
                                );
            """
        ),
    ]
