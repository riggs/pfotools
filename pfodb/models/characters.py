# -*- coding: utf-8 -*-
from django.db import models

__all__ = ('Feat', )


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


