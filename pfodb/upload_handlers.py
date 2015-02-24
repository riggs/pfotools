
from openpyxl import load_workbook

from pfodb.models import *


def _get(Model, **kwargs):
    pk_name = Model._meta.pk.name
    query = dict()
    if pk_name in kwargs:
        query[pk_name] = kwargs[pk_name]
    elif Model._meta.unique_together:
        for unique in Model._meta.unique_together:
            for field in unique:
                if field in kwargs:
                    query[field] = kwargs[field]
    else:
        for field in filter(lambda x: x.unique, Model._meta.fields):
            if field in kwargs:
                query[field] = kwargs[field]
    try:
        item = Model.objects.get(**query)
    except Model.DoesNotExist:
        item = Model(**kwargs)
        item.save()
    return item


def import_from_PFO_wiki_data(_file):
    wb = load_workbook(_file)
    crafting = wb.get_sheet_by_name('Recipes (Crafting)')
    refining = wb.get_sheet_by_name('Recipes (Refining)')

    for row in refining.rows[1:]:
        (_0,    # Ignore full name
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
         ) = (cell.value for cell in row)   # Unpack

        if not _0:  # Empty row
            continue

        feat = _get(Feat, name=feat_name, rank=feat_rank)

        recipe = _get(Refining_Recipe, name=name, plus_value=plus_value, tier=tier, required_feat=feat,
                      output_quantity=output_quantity, base_crafting_seconds=base_crafting_seconds,
                      achievement_type=achievement_type)

        component = _get(Component, name=name, plus_value=plus_value, tier=tier, variety=variety, quality=quality,
                         recipe=recipe)

        for element_name, quantity in zip((e1, e2, e3, e4), (q1, q2, q3, q4)):
            if element_name is None:
                continue
            element = _get(Ingredient, name=element_name, tier=quality)
            measure = _get(Refining_Bill_Of_Materials, recipe=recipe, material=element, quantity=quantity)

    retries = []
    def _create_crafting_measure(recipe, ingredient_name, quantity):
        try:
            ingredient = Component.objects.get(name=ingredient_name, plus_value=0)
        except Component.DoesNotExist:
            try:
                ingredient = Item.objects.get(name=ingredient_name, plus_value=0)
            except Item.DoesNotExist:
                retries.append((recipe, ingredient_name, quantity))
                return
        return _get(Crafting_Bill_Of_Materials, recipe=recipe, object_id=ingredient.id, material=ingredient, quantity=quantity)

    for row in crafting.rows[1:]:
        (_0,    # Ignore full name
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

        if not _0:  # Empty row
            continue

        feat = _get(Feat, name=feat_name, rank=feat_rank)

        recipe = _get(Crafting_Recipe, name=name, tier=tier, required_feat=feat, output_quantity=output_quantity,
                      base_crafting_seconds=base_crafting_seconds, achievement_type=achievement_type)

        item = _get(Item, name=name, plus_value=0, tier=tier, category=category, quality=quality, recipe=recipe)

        for ingredient_name, quantity in zip((c1, c2, c3, c4), (q1, q2, q3, q4)):
            if ingredient_name is None:
                continue
            measure = _create_crafting_measure(recipe, ingredient_name, quantity)

    while len(retries):
        _create_crafting_measure(*retries.pop())
