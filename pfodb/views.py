# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from . import models


class Industry_Index(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('For all your industrious needs.')


class Item(View):

    def get(self, request, *args, **kwargs):
        query = kwargs.get('query')
        if not query:
            return HttpResponse('Search for items in the url, e.g. crafting/bow')
        elif query == 'all':
            items = models.Equipment.objects.all()
        else:
            filter_kwargs = dict(name__icontains=query.strip())
            items = models.Equipment.objects.filter(**filter_kwargs)
        return HttpResponse(
            "<br>".join(
                "{name} ({feat}): {ingredients}".format(
                    name=item.name, feat=item.recipe.required_feat,
                    ingredients=", ".join(
                        '''{quantity} <a href=../refining/{url_name}>{name}</a>'''.format(
                            quantity=ingredient.quantity, name=ingredient.material.name,
                            url_name=ingredient.material.name.replace(' ', '%20'))
                        for ingredient in item.recipe.materials.all()))
                for item in items))


class Component(View):

    def get(self, request, *args, **kwargs):
        query = kwargs.get('query')
        if not query:
            return HttpResponse('Search for items in the url, e.g. refining/oak')
        elif query == 'all':
            items = models.Refined_Material.objects.all()
        else:
            filter_kwargs = dict(name__icontains=query.strip())
            plus_value = kwargs.get('plus_value')
            if plus_value is not None:
                filter_kwargs['plus_value'] = int(plus_value)
            items = models.Refined_Material.objects.filter(**filter_kwargs)
        return HttpResponse(
            "<br>".join(
                "{name} +{plus_value} ({feat}): {ingredients}, makes {quantity}".format(
                    name=item.name, plus_value=item.plus_value, feat=item.recipe.required_feat,
                    ingredients=", ".join(
                        '{quantity} {name}'.format(quantity=ingredient.quantity, name=ingredient.material.name)
                        for ingredient in item.recipe.materials.all()),
                    quantity=item.recipe.output_quantity, )
                for item in items))
