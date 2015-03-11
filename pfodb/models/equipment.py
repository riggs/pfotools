# -*- coding: utf-8 -*-
"""
ORM Models used to represent gathered, looted, & crafted items in PFO.

Some models are used to automatic generation of a (simple) REST API.
"""
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from .characters import Feat
from ..rest_api.serializers import *
from ..rest_api import publish, RANKING_FIELDS

RANKING_FIELDS.add('plus_value')

from ..utils import public
# __all__ defined by the @public decorator on objects


class Plussed(models.Model):
    """Django Abstract Base Class model for entries indexed by name & plus value."""
    name = models.CharField(max_length=120)
    plus_value = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "{name} +{plus}".format(name=self.name, plus=self.plus_value)

    class Meta:
        abstract = True
        unique_together = \
        index_together = ('name', 'plus_value')


class Named(models.Model):
    """Django Abstract Base Class model for entries with name as primary key."""
    name = models.CharField(max_length=120, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Tiered(models.Model):
    """Django Abstract Base Class mixin for entries with tier levels."""
    tier = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True


@publish(sources=sources, path='raw_ingredients', ingredient_of=ingredient_of, name=name, url=url)
@public
class Raw_Ingredient(Named):
    """Abstract designation used to determine which ingredients fulfill a recipe."""


@publish('tier', 'variety', 'encumbrance', ingredients=ingredients, path='raw_materials', name=name, url=url)
@public
class Raw_Material(Named, Tiered):
    """Raw material, either gathered or looted."""
    ingredients = models.ManyToManyField(Raw_Ingredient, related_name='sources')
    variety = models.CharField(max_length=120)
    encumbrance = models.FloatField()


@publish('tier', sources=sources, ingredient_of=ingredient_of, path='refined_ingredients', name=name, url=url)
@public
class Refined_Ingredient(Named, Tiered):
    """Abstract designation used to determine which ingredients fulfill a recipe."""
    ingredient_of = GenericRelation('Crafting_Bill_Of_Materials')


@publish('tier', 'variety', 'quality', plus='plus_value', recipe=recipe, path='refined_materials', name=name, url=url)
@public
class Refined_Material(Plussed, Tiered):
    """Specific outputs from refining process."""
    variety = models.CharField(max_length=120)
    quality = models.PositiveIntegerField()
    recipe = models.OneToOneField('Refining_Recipe', related_name='output')
    ingredient = models.ForeignKey(Refined_Ingredient, related_name='sources')


@publish('tier', 'category', 'quality', recipe=recipe, ingredient_of=ingredient_of, name=name, url=url)
@public
class Equipment(Named, Tiered):
    """Types of things usable by characters. To reference actual things at a later date."""
    category = models.CharField(max_length=120)
    quality = models.PositiveIntegerField()
    recipe = models.OneToOneField('Crafting_Recipe', related_name='output')
    ingredient_of = GenericRelation('Crafting_Bill_Of_Materials')


@publish(name=name, url=url)  # Lack of fields provides namespace for subclasses only.
class Recipe(models.Model):
    """Django Abstract Base Class model for Recipes. Subclass & define 'ingredients' & 'output'."""
    required_feat = models.ForeignKey(Feat)     # Includes rank

    output_quantity = models.PositiveIntegerField()

    base_crafting_seconds = models.PositiveIntegerField()
    achievement_type = models.CharField(max_length=120)

    class Meta:
        abstract = True


@publish('tier', 'base_crafting_seconds', 'output_quantity', 'achievement_type', plus='plus_value',
         feat=required_feat, materials=materials, path='refining', name=name, url=url)
@public
class Refining_Recipe(Plussed, Tiered, Recipe):
    """Recipes to turn raw materials into component ingredients for crafting."""
    # materials = 'defined via ForeignKey on Refining_Bill_Of_Materials'
    # output = 'defined via ForeignKey on Refined_Material'


@publish('tier', 'base_crafting_seconds', 'output_quantity', 'achievement_type',
         feat=required_feat, materials=materials, path='crafting', name=name, url=url)
@public
class Crafting_Recipe(Named, Tiered, Recipe):
    """Recipes to turn ingredients into usable items."""
    # materials = 'defined via ForeignKey on Crafting_Bill_Of_Materials'
    # output = 'defined via ForeignKey on Equipment'


@public
class Refining_Bill_Of_Materials(models.Model):
    """Intermediary table for many-to-many relationship between Refining Recipes and Elements."""
    recipe = models.ForeignKey(Refining_Recipe, related_name='materials', related_query_name='material')
    material = models.ForeignKey(Raw_Ingredient, related_name='ingredient_of')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return "{quantity} {material} ({recipe})".format(recipe=self.recipe, quantity=self.quantity,
                                                         material=self.material)

    class Meta:
        unique_together = ('recipe', 'material')


@public
class Crafting_Bill_Of_Materials(models.Model):
    """Intermediary table for many-to-many relationship between Crafting Recipes and Items."""
    recipe = models.ForeignKey(Crafting_Recipe, related_name='materials', related_query_name='material')

    content_type = models.ForeignKey(ContentType)
    object_id = models.CharField(max_length=120)
    material = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField()

    def __str__(self):
        return "{quantity} {material} ({recipe})".format(recipe=self.recipe, quantity=self.quantity,
                                                         material=self.material)

    class Meta:
        unique_together = ('recipe', 'object_id', 'content_type')

