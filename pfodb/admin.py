# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from .models.metadata import Worksheet


admin.site.register(Feat)
admin.site.register(Raw_Ingredient)
admin.site.register(Raw_Material)
admin.site.register(Refined_Ingredient)
admin.site.register(Refined_Material)
admin.site.register(Equipment)
admin.site.register(Refining_Recipe)
admin.site.register(Crafting_Recipe)
admin.site.register(Refining_Bill_Of_Materials)
admin.site.register(Crafting_Bill_Of_Materials)

admin.site.register(Worksheet)
