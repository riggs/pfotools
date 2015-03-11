# -*- coding: utf-8 -*-
"""
Functions to serialize attributes on models
"""
from operator import attrgetter

from .utils import name_and_url, get_entry_url

from ..utils import public
# __all__ defined by the @public decorator on objects


@public
def foreign_key_field(field):
    getter = attrgetter(field)
    def serializer(entry, request, namespaces):
        return name_and_url(getter(entry), request, namespaces)
    return serializer


@public
def reverse_foreign_keys(field):
    getter = attrgetter(field)
    def serializer(entry, request, namespaces):
        return [name_and_url(item, request, namespaces) for item in getter(entry).all()]
    return serializer


@public
def ingredient_of(entry, request, namespaces):
    return [name_and_url(use.recipe, request, namespaces) for use in entry.ingredient_of.all()]


@public
def materials(entry, request, namespaces):
    return [{'ingredient': name_and_url(bom.material, request, namespaces),
             'quantity': bom.quantity} for bom in entry.materials.all()]


@public
def name(entry, *_):
    return str(entry)


@public
def url(entry, request, namespaces):
    return get_entry_url(entry, request, namespaces)
