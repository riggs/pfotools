# -*- coding: utf-8 -*-
from datetime import datetime, timezone, timedelta

from django.db import models as models


class Worksheet(models.Model):
    name = models.CharField(max_length=120, primary_key=True)
    updated = models.DateTimeField(default=datetime.utcfromtimestamp(0).replace(tzinfo=timezone(timedelta(0))))
