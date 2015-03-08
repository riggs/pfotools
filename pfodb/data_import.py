# -*- coding: utf-8 -*-
from openpyxl import load_workbook

from django.contrib.contenttypes.models import ContentType

from pfodb.models import *


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


def import_from_PFO_wiki_data(_file):
    wb = load_workbook(_file)
    crafting = wb.get_sheet_by_name('Recipes (Crafting)')
    refining = wb.get_sheet_by_name('Recipes (Refining)')

    for row in refining.rows[1:]:   # Skip row with column headers
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
         ) = (cell.value for cell in row)   # Unpack values in cells, assign to variables

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
            if ingredient_name is None:
                continue
            raw_ingredient, _ = Raw_Ingredient.objects.update_or_create(name=ingredient_name,
                                                                        defaults=dict(tier=quality))
            measure, _ = Refining_Bill_Of_Materials.objects.update_or_create(recipe=recipe, material=raw_ingredient,
                                                                             defaults=dict(quantity=quantity))

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

    for row in crafting.rows[1:]:   # Skip row with column headers
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
         ) = (cell.value for cell in row)   # Unpack

        if not __:  # Empty row
            continue

        feat, _ = Feat.objects.update_or_create(name=feat_name, rank=feat_rank)

        recipe, _ = Crafting_Recipe.objects.update_or_create(name=name,
                                                             defaults=dict(tier=tier, required_feat=feat,
                                                                           output_quantity=output_quantity,
                                                                           base_crafting_seconds=base_crafting_seconds,
                                                                           achievement_type=achievement_type))

        item, _ = Equipment.objects.update_or_create(name=name, defaults=dict(tier=tier, category=category,
                                                                              quality=quality, recipe=recipe))

        for ingredient_name, quantity in zip((c1, c2, c3, c4), (q1, q2, q3, q4)):
            if ingredient_name is None:
                continue
            measure = _create_crafting_measure(recipe, ingredient_name, quantity)

    # Iteratively attempt to add entries to database that were unable to be added previously.  Circular dependencies
    # will cause RuntimeError('maximum recursion depth exceeded'), but database will be otherwise populated.
    while len(retries):
        _create_crafting_measure(*retries.pop())
