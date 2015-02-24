from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


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
    """Django Abstract Base Class model for entries with tier levels."""
    tier = models.PositiveIntegerField(default=1,
                                       choices=((1, 'I'), (2, 'II'), (3, 'III')))

    class Meta:
        abstract = True


class Feat(Named):
    """All the things characters can train."""
    # Prerequisites, trainer, ability score, etc. to come later.


class Element(Named):
    """Abstract designation used to determine which ingredients fulfill a recipe."""


class Raw_Material(Named):
    """Raw material, either gathered or looted."""
    elements = models.ManyToManyField(Element, related_name='sources', related_query_name='source')


class Component_Material(Named):
    """Output material from refining process."""


class Component(Plussed, Tiered):
    """Specific outputs from refining process."""
    material = models.ForeignKey(Component_Material)


class Item_Type(Named):
    """Output from crafting process."""


class Item(Plussed, Tiered):
    """Things usable by characters"""
    type = models.ForeignKey(Item_Type)


class Recipe(models.Model):
    """Django Abstract Base Class model for Recipes. Subclass & define 'ingredients' & 'output'."""
    required_feat = models.ForeignKey(Feat)
    required_feat_rank = models.PositiveIntegerField(default=0)


    output_quantity = models.PositiveIntegerField(default=1)

    base_crafting_seconds = models.PositiveIntegerField()
    quality = models.PositiveIntegerField()
    category = models.CharField(max_length=120)
    achievement_type = models.CharField(max_length=120)

    class Meta:
        abstract = True


class Refining_Measure(models.Model):
    """Intermediary table for many-to-many relationship between Refining Recipes and Elements."""
    recipe = models.ForeignKey('Refining_Recipe', related_name='elements', related_query_name='element')
    material = models.ForeignKey(Element, related_name='measures', related_query_name='measure')
    quantity = models.PositiveIntegerField(default=1)


class Refining_Recipe(Plussed, Tiered, Recipe):
    """Recipes to turn raw materials into component ingredients for crafting."""
    ingredients = models.ManyToManyField(Element, through=Refining_Measure, related_name='used_by')
    output = models.OneToOneField(Component, related_name='recipes', related_query_name='recipe')


class Crafting_Measure(models.Model):
    """Intermediary table for many-to-many relationship between Crafting Recipes and Items."""
    recipe = models.ForeignKey('Crafting_Recipe', related_name='elements', related_query_name='element')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    material = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(default=1)


class Crafting_Recipe(Named, Tiered, Recipe):
    """Recipes to turn ingredients into usable items."""
    ingredients = GenericRelation(Crafting_Measure, related_query_name='recipes')
    output = models.OneToOneField(Item, related_name='recipes', related_query_name='recipe')

