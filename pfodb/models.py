from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Plussed(models.Model):
    """Django Abstract Base Class model for entries indexed by name & plus value."""
    name = models.CharField(max_length=120)
    plus_value = models.PositiveIntegerField(blank=True)

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


class Component(Plussed, Tiered):
    """Output from refining process."""


class Item(Plussed, Tiered):
    """Output from crafting process."""


class Raw_Material(Named):
    """Raw material, either gathered or looted."""
    elements = models.ManyToManyField(Element, related_name='sources', related_query_name='source')


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


class Refining_Recipe(Plussed, Tiered, Recipe):
    """Recipes to turn raw materials into component ingredients for crafting."""
    ingredients = models.ManyToManyField(Element, through='Element_Measure', related_name='used_by')
    output = models.OneToOneField(Component, related_name='component_recipe')


class Element_Measure(models.Model):
    """Intermediary table for many-to-many relationship between Refining Recipes and Elements."""
    recipe = models.ForeignKey(Refining_Recipe, related_name='elements', related_query_name='element')
    material = models.ForeignKey(Element, related_name='measures', related_query_name='measure')
    quantity = models.PositiveIntegerField(default=1)


class Crafting_Recipe(Named, Tiered, Recipe):
    """Recipes to turn ingredients into usable items."""
    ingredients = GenericRelation('Crafted_Item_Measure', related_query_name='recipes')


class Crafted_Item_Measure(models.Model):
    """Intermediary table for many-to-many relationship between Crafting Recipes and Crafted Items."""
    recipe = models.ForeignKey(Crafting_Recipe, related_name='elements', related_query_name='element')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    material = GenericForeignKey('content_type', 'object_id')

    quantity = models.PositiveIntegerField(default=1)
