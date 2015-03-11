# -*- coding: utf-8 -*-

import os
import gspread
from configparser import ConfigParser
from datetime import datetime, timezone, timedelta

from django.contrib.contenttypes.models import ContentType

from .models import *
from .models.metadata import Worksheet


worksheet_handlers = {}
def worksheet(*names):
    def passthrough(func):
        for name in names:
            worksheet_handlers[name] = func
        return func
    return passthrough


def __update_or_create(Model, **kwargs):
    """
    Turns out this is unneeded because of Model.object.update_or_create.

    And needed again because of a strange interaction with GenericForeignKey.
    Fixed: content_type=ContentType.objects.get_for_model(ingredient)

    Update and return Model entry as specified by kwargs.

    :param Model: Django DB Model to query.
    :param kwargs: named values used to retrieve and update DB entry.
    :return:
    """
    pk_name = Model._meta.pk.name
    # Remove primary key, if any.  This enables kwargs can be used for updates, later.
    pk_value = kwargs.pop(pk_name, None)
    query = dict()
    if pk_value:
        query[pk_name] = pk_value
    elif Model._meta.unique_together:
        # PK not given.  Look for kwargs combos that satisfies Model's unique constraints to use as query.
        for unique in Model._meta.unique_together:
            for field in unique:
                try:
                    query[field] = kwargs[field]
                except KeyError:    # Need to add all or none of the fields for a unique combo to query.
                    query.clear()
                    break
    if not query:
        # PK not given, unique combinations not found.  Look for kwargs matching unique fields on Model.
        for field in filter(lambda x: x.unique, Model._meta.fields):
            if field in kwargs:
                query[field] = kwargs[field]
    try:
        item = Model.objects.get(**query)
        # Modify item values according to given kwargs, if item is found via query.
        for k, v in kwargs.items():
            setattr(item, k, v)
    except Model.DoesNotExist:
        # Nothing found in Model table matching kwargs, so create an entry.
        item = Model(**kwargs)
    item.save()
    return item


@worksheet('Recipes (Refining)')
def import_refining(worksheet):

    for row in worksheet.get_all_values()[1:]:   # Skip row with column headers
        (__,    # Full name, used only to ensure row has data
         feat_name,
         feat_rank,
         tier,
         e1,
         q1,
         e2,
         q2,
         e3,
         q3,
         e4,
         q4,
         name,
         plus_value,
         output_quantity,
         base_crafting_seconds,
         quality,
         variety,
         achievement_type,
         *_     # Ignore the rest
         ) = row   # Unpack values in cells, assign to variables

        if not __:  # Empty row
            continue

        feat, _ = Feat.objects.update_or_create(name=feat_name, rank=feat_rank)

        recipe, _ = Refining_Recipe.objects.update_or_create(name=name, plus_value=plus_value,
            defaults=dict(tier=tier, required_feat=feat, output_quantity=output_quantity,
                          base_crafting_seconds=base_crafting_seconds, achievement_type=achievement_type))

        refined_ingredient, _ = Refined_Ingredient.objects.update_or_create(name=name, tier=tier)

        refined_material, _ = Refined_Material.objects.update_or_create(name=name, plus_value=plus_value,
            defaults=dict(tier=tier, variety=variety, quality=quality, recipe=recipe, ingredient=refined_ingredient))

        for ingredient_name, quantity in zip((e1, e2, e3, e4), (q1, q2, q3, q4)):
            if not ingredient_name:
                continue
            raw_ingredient, _ = Raw_Ingredient.objects.update_or_create(name=ingredient_name)
            measure, _ = Refining_Bill_Of_Materials.objects.update_or_create(recipe=recipe, material=raw_ingredient,
                                                                             defaults=dict(quantity=quantity))


@worksheet('Recipes (Crafting)')
def import_crafting(worksheet):

    # Some recipes require finished items as ingredients, and those ingredients may not be in the database, yet.
    # Record spreadsheet entries that fail to find all of their ingredients.  Later, retry adding these entries to the
    # database since the items they depend upon should have since been added.
    retries = []
    def _create_crafting_measure(recipe, ingredient_name, quantity):
        try:
            ingredient = Refined_Ingredient.objects.get(name=ingredient_name)
        except Refined_Ingredient.DoesNotExist:
            try:
                ingredient = Equipment.objects.get(name=ingredient_name)
            except Equipment.DoesNotExist:
                retries.append((recipe, ingredient_name, quantity))
                return
        return Crafting_Bill_Of_Materials.objects.update_or_create(
            recipe=recipe, object_id=ingredient.pk, content_type=ContentType.objects.get_for_model(ingredient),
            defaults=dict(quantity=quantity))

    for row in worksheet.get_all_values()[1:]:   # Skip row with column headers
        (__,    # Full name, used only to ensure row has data
         feat_name,
         feat_rank,
         tier,
         c1,
         q1,
         c2,
         q2,
         c3,
         q3,
         c4,
         q4,
         name,
         _,     # Ignore empty column
         output_quantity,
         base_crafting_seconds,
         category,
         quality,
         achievement_type,
         *_     # Ignore the rest
         ) = row   # Unpack

        if not __:  # Empty row
            continue

        feat, _ = Feat.objects.update_or_create(name=feat_name, rank=feat_rank)

        recipe, _ = Crafting_Recipe.objects.update_or_create(
            name=name, defaults=dict(tier=tier, required_feat=feat, output_quantity=output_quantity,
                                     base_crafting_seconds=base_crafting_seconds, achievement_type=achievement_type))

        item, _ = Equipment.objects.update_or_create(name=name, defaults=dict(tier=tier, category=category,
                                                                              quality=quality, recipe=recipe))

        for ingredient_name, quantity in zip((c1, c2, c3, c4), (q1, q2, q3, q4)):
            if not ingredient_name:
                continue
            measure = _create_crafting_measure(recipe, ingredient_name, quantity)

    # Iteratively attempt to add entries to database that were unable to be added previously.  Circular dependencies
    # will cause RuntimeError('maximum recursion depth exceeded'), but database will be otherwise populated.
    while len(retries):
        _create_crafting_measure(*retries.pop())


@worksheet('Raw Resources', 'Raw Salvage')
def import_raw_materials(worksheet):
    for row in worksheet.get_all_values()[1:]:   # Skip row with column headers
        (resource_name,    # Full name, used only to ensure row has data
         variety,
         tier,
         encumbrance,
         ingredient1,
         ingredient2,
         *_     # Ignore the rest
        ) = row   # Unpack values in cells, assign to variables

        if not resource_name:  # Empty row
            continue

        raw_material, _ = Raw_Material.objects.update_or_create(
            name=resource_name, defaults=dict(tier=tier, variety=variety, encumbrance=encumbrance))

        for ingredient in (ingredient1, ingredient2):
            if not ingredient:
                continue
            raw_ingredient, _ = Raw_Ingredient.objects.update_or_create(name=ingredient)
            raw_material.ingredients.add(raw_ingredient)


def update_tables(*args, **kwargs):
    email = os.environ.get('PFODB_GSPREAD_EMAIL')
    if email is not None:
        try:
            gc = gspread.login(email, os.environ.get('PFODB_GSPREAD_PASSWORD'))
        except gspread.AuthenticationError:
            raise RuntimeError('Invalid credentials, unable to access spreadsheets.')
    else:
        config = ConfigParser()
        if not config.read('credentials.ini'):
            raise RuntimeError('No credentials available, unable to access spreadsheets.')
        try:
            gc = gspread.login(**config['gspread'])
        except gspread.AuthenticationError:
            raise RuntimeError('Invalid credentials, unable to access spreadsheets.')

    sheets = [
        '1UsN8eNlnD7iM_XcFYRvVJJDGTM-0ShcOTQyGcgrxqA0',
        '151PH3vBnlnLWYH3rv3kqAUVJg0OLOLnItqeBxc2vhEA',
    ]

    for sheet in sheets:
        spreadsheet = gc.open_by_key(sheet)

        for worksheet in spreadsheet.worksheets():
            title = worksheet.title
            record, created = Worksheet.objects.update_or_create(name=title)
            if created:
                print("Created", record.name)
            updated = datetime.strptime(worksheet.updated, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone(timedelta(0)))
            if updated > record.updated:
                handler = worksheet_handlers.get(title)
                if handler is not None:
                    handler(worksheet)
                    record.updated = updated
                    record.save()


