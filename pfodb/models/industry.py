# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from .characters import Feat

__all__ = ('Ingredient', 'Raw_Material', 'Component', 'Item', 'Refining_Recipe', 'Crafting_Recipe',
           'Refining_Bill_Of_Materials', 'Crafting_Bill_Of_Materials', )


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
    tier = models.PositiveIntegerField(default=1,
                                       choices=((1, 'I'), (2, 'II'), (3, 'III')))

    class Meta:
        abstract = True


class Ingredient(Named, Tiered):
    """Abstract designation used to determine which ingredients fulfill a recipe."""


class Raw_Material(Named, Tiered):
    """Raw material, either gathered or looted."""
    elements = models.ManyToManyField(Ingredient)


class Component(Plussed, Tiered):
    """Specific outputs from refining process."""
    variety = models.CharField(max_length=120)
    quality = models.PositiveIntegerField()
    recipe = models.OneToOneField('Refining_Recipe', related_name='output')
    used_by = GenericRelation('Crafting_Bill_Of_Materials')

    class Meta(Plussed.Meta):
        unique_together = Plussed.Meta.unique_together + ('recipe',)


class Item(Plussed, Tiered):
    """Things usable by characters"""
    category = models.CharField(max_length=120)
    quality = models.PositiveIntegerField()
    recipe = models.ForeignKey('Crafting_Recipe', related_name='outputs', related_query_name='output')
    used_by = GenericRelation('Crafting_Bill_Of_Materials')


class Recipe(models.Model):
    """Django Abstract Base Class model for Recipes. Subclass & define 'ingredients' & 'output'."""
    required_feat = models.ForeignKey(Feat)

    output_quantity = models.PositiveIntegerField()

    base_crafting_seconds = models.PositiveIntegerField()
    achievement_type = models.CharField(max_length=120)

    class Meta:
        abstract = True


class Refining_Recipe(Plussed, Tiered, Recipe):
    """Recipes to turn raw materials into component ingredients for crafting."""
    ingredients = models.ManyToManyField(Ingredient, through='Refining_Bill_Of_Materials', related_name='used_by')


class Crafting_Recipe(Named, Tiered, Recipe):
    """Recipes to turn ingredients into usable items."""
    ingredients = GenericRelation('Crafting_Bill_Of_Materials', related_query_name='recipes')


class Refining_Bill_Of_Materials(models.Model):
    """Intermediary table for many-to-many relationship between Refining Recipes and Elements."""
    recipe = models.ForeignKey(Refining_Recipe, related_name='elements', related_query_name='element')
    material = models.ForeignKey(Ingredient, related_name='components', related_query_name='component')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return "{quantity} {material} ({recipe})".format(recipe=self.recipe, quantity=self.quantity,
                                                        material=self.material)

    class Meta:
        unique_together = ('recipe', 'material')


class Crafting_Bill_Of_Materials(models.Model):
    """Intermediary table for many-to-many relationship between Crafting Recipes and Items."""
    recipe = models.ForeignKey(Crafting_Recipe, related_name='ingredients', related_query_name='ingredient')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    material = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField()

    def __str__(self):
        return "{quantity} {material} ({recipe})".format(recipe=self.recipe, quantity=self.quantity,
                                                        material=self.material)

    class Meta:
        unique_together = ('recipe', 'object_id')

