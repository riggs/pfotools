# -*- coding: utf-8 -*-
from django.db import models

from ..rest_api.serializers import *
from ..rest_api import publish, RANKING_FIELDS
RANKING_FIELDS.add('rank')

from ..utils import public
# __all__ defined by the @public decorator on objects


@publish('rank', path='feats', name=name, url=url)
@public
class Feat(models.Model):
    """All the things characters can train."""
    name = models.CharField(max_length=120)
    rank = models.PositiveIntegerField(default=0)
    # Prerequisites, trainer, ability score, etc. to come later.

    def __str__(self):
        return "{name} {rank}".format(name=self.name, rank=self.rank)

    class Meta:
        unique_together = \
        index_together = ('name', 'rank')

