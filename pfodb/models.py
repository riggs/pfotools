from django.db import models


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


class Feat(Named):
    """All the things characters can train."""
    # Prerequisites, trainer, ability score, etc. to come later.


class Element(Named):
    """Abstract designation used to determine which ingredients fulfill a recipe."""


class Component(Plussed):
    """Output from refining process."""


class Item(Component):
    """Output from crafting process."""


class Raw_Material(Named):
    """Raw material, either gathered or looted."""
    elements = models.ManyToManyField(Element, related_name='sources', related_query_name='source')


def _recipe_factory(ingredient_table, output_table):
    class Recipe(models.Model):
        required_feat = models.ForeignKey(Feat)
        required_feat_rank = models.PositiveIntegerField(default=0)

        tier = models.PositiveIntegerField(default=1)

        ingredients = models.ManyToManyField(ingredient_table,
                                             through='{name}_Measure'.format(name=ingredient_table.__name__),
                                             related_name='uses',
                                             related_query_name='usage')

        output = models.OneToOneField(output_table,
                                      related_name='{name}_recipe'.format(name=output_table.__name__))
        output_quantity = models.PositiveIntegerField(default=1)

        base_crafting_seconds = models.PositiveIntegerField()
        quality = models.PositiveIntegerField()
        category = models.CharField(max_length=120)
        achievement_type = models.CharField(max_length=120)

        class Meta:
            abstract = True

    return Recipe


class Refining_Recipe(Plussed, _recipe_factory(Element, Component)):
    """Recipes to turn raw materials into component ingredients for crafting."""


class Crafting_Recipe(Named, _recipe_factory(Item, Item)):
    """Recipes to turn ingredients into usable items."""


def _intermediary_factory(recipe_table, ingredient_table):
    class Intermediary(models.Model):
        recipe = models.ForeignKey(recipe_table,
                                   related_name='{name}s'.format(name=ingredient_table.__name__),
                                   related_query_name='{name}'.format(name=ingredient_table.__name__))
        material = models.ForeignKey(ingredient_table, related_name='measures', related_query_name='measure')
        quantity = models.PositiveIntegerField(default=1)

        class Meta:
            abstract = True

    return Intermediary


class Element_Measure(_intermediary_factory(Refining_Recipe, Element)):
    """Intermediary table for many-to-many relationship between Refining Recipes and Elements."""


class Item_Measure(_intermediary_factory(Crafting_Recipe, Item)):
    """Intermediary table for many-to-many relationship between Crafting Recipes and Items."""
