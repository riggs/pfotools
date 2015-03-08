# -*- coding: utf-8 -*-
"""
Functions to serialize attributes on models
"""
from .utils import name_and_url, get_entry_url

from ..utils import public
# __all__ defined by the @public decorator on objects


@public
def used_by(entry, request, namespaces):
    return [name_and_url(use.recipe, request, namespaces) for use in entry.used_by.all()]


@public
def required_feat(entry, request, namespaces):
    return name_and_url(entry.required_feat, request, namespaces)


@public
def materials(entry, request, namespaces):
    return [{'ingredient': name_and_url(bom.material, request, namespaces),
             'quantity': bom.quantity} for bom in entry.materials.all()]


@public
def recipe(entry, request, namespaces):
    return name_and_url(entry.recipe, request, namespaces)


@public
def ingredients(entry, request, namespaces):
    return [name_and_url(ingredient, request, namespaces) for ingredient in entry.ingredients.all()]


@public
def sources(entry, request, namespaces):
    return [name_and_url(source, request, namespaces) for source in entry.sources.all()]


@public
def name(entry, request, namespaces):
    return str(entry)


@public
def url(entry, request, namespaces):
    return get_entry_url(entry, request, namespaces)
