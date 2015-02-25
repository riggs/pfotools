# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from . import models

__all__ = ('Industry_Index', 'Item', 'Component',
)

class Industry_Index(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('For all your industrious needs.')


class Item(View):

    def get(self, request, *args, **kwargs):
        query = kwargs.get('query')
        if query:
            return HttpResponse(
                "<br>".join(
                    "{name} +0: {ingredients}".format(
                        name=item.name, ingredients=", ".join(
                            '{quantity} {name}'.format(quantity=ingredient.quantity, name=ingredient.material.name)
                            for ingredient in item.recipe.bill_of_materials.all()))
                    for item in models.Item.objects.filter(name__icontains=query)))
        return HttpResponse('Search for items in the url, e.g. crafting/bow')


class Component(View):

    def get(self, request, *args, **kwargs):
        query = kwargs.get('query')
        plus_value = kwargs.get('plus_value')
        if query:
            return HttpResponse(
                "<br>".join(
                    "{name} +{plus_value}: {ingredients}".format(
                        name=item.name, plus_value=item.plus_value, ingredients=", ".join(
                            '{quantity} {name}'.format(quantity=ingredient.quantity, name=ingredient.material.name)
                            for ingredient in item.recipe.bill_of_materials.all()))
                    for item in models.Component.objects.filter(name__icontains=query)))
        return HttpResponse('Search for items in the url, e.g. refining/oak')
