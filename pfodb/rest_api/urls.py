# -*- coding: utf-8 -*-

from pprint import pprint

import json

from django.conf.urls import include, patterns, url
from django.http import HttpResponse, HttpResponseNotFound

from .utils import *
from ..utils import public
# __all__ defined by the @public decorator on objects


# Import and add field names to allow specifying numerical 'level' of object in URL.
RANKING_FIELDS = public(RANKING_FIELDS=set())


def render_json(data):
    return HttpResponse(json.dumps(data), content_type='application/json')


def render404_json(message):
    return HttpResponseNotFound(json.dumps(message), content_type='application/json')


def get_or_call_attr(obj, attr, request, namespaces):
    return attr(obj, request, namespaces) if callable(attr) else getattr(obj, attr)


def build_urls(tree, namespaces):
    tree = tree.copy()
    urls = []
    Model = tree.pop('Model', None)
    namespace = namespaces.get(Model, namespaces['root'])
    fields = tree.pop('fields', [])

    if Model is None or Model._meta.abstract:
        # Either at top of tree or Model exists only for namespace purposes.
        def response(request):
            paths = []
            for path, node in tree.items():
                M = node['Model']
                namespaces.setdefault(M, namespace + (path,))
                paths.append(name_and_url(M, request, namespaces))
            return render_json({'paths': paths})

    else:
        # Model represents actual data to return.
        # If given no specific entry name, return a listing of all entries, but only name & plus (if applicable).
        # Otherwise try to find named entry & return it, filtered by rank, if given.
        def response(request, **kwargs):
            name = kwargs.get('name')
            rank = kwargs.get('rank')
            filter_kwargs = {}
            if name is not None:
                filter_kwargs['name__iexact'] = name.strip()
            if rank is not None:
                for ranking in RANKING_FIELDS:
                    if ranking in Model._meta.get_all_field_names():
                        filter_kwargs[ranking] = int(rank)
                        break
            data = Model.objects.filter(**filter_kwargs)

            if len(data) == 0:
                return render404_json('No {Model} called {query}'.format(
                                        Model=Model.__name__, query=name if not rank else name + ' +' + rank))

            if name is None or len(data) > 1:   # Only return identifier & URL instead of all stats
                data = [name_and_url(entry, request, namespaces) for entry in data]
            else:
                data = [dict((name, get_or_call_attr(entry, value, request, namespaces))
                             for name, value in fields.items())
                        for entry in data]

            return render_json(data)

    urls.append(url(r'^$', response, name='index'))  # Return either {'path': <subpath list>} or all names (& pluses).

    for path, node in tree.items():     # Add any sub-paths before open-ended regex.
        namespaces.setdefault(node['Model'], namespace + (path,))
        urls.append(url(r'^{path}/'.format(path=path),
                        include(build_urls(node, namespaces), namespace=path, app_name='pfodb')))

    if Model is not None and not Model._meta.abstract:
        urls.append(url(r"^"
                         # Match 'name' to any combination of letters, space and single-quote, as 'name'
                         "(?P<name>("
                            "[^\W\d]|[ ']"     # [Not (not-alphanumerics or digits)] or [space or single-quote]
                         ")+)"
                         "(\+?(?P<rank>\d))?$",         # Match optional '+2' with 2 as 'rank'
                        response))
    return patterns('', *urls)


@public
def generate_urls(*namespaces):
    namespaces = {'root': namespaces}
    return build_urls(generate_tree(publish.for_publication), namespaces)
