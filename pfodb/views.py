# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from .models import *

__all__ = ('Industry_Index', 'Item',
)

class Industry_Index(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('For all your industrious needs.')


class Item(View):

    def get(self, request, *args, **kwargs):
        query = kwargs.get('query')
        if query:
            return HttpResponse(
                "\n".join(
                    ", ".join(
                        '{quantity} {name}'.format(quantity=ingredient.quantity, name=ingredient.material.name)
                        for ingredient in item.recipe.ingredients.all())
                    for item in Item.objects.filter(name__icontains=query)))
        return HttpResponse('Search for items in the url, e.g. items/bow')
