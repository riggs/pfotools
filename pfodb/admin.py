from django.contrib import admin
from pfodb.models import (Feat, Element, Raw_Material, Component_Material, Component, Item_Type, Item, Refining_Measure,
                          Refining_Recipe, Crafting_Measure, Crafting_Recipe,
                          )


admin.site.register(Feat)
admin.site.register(Element)
admin.site.register(Raw_Material)
admin.site.register(Component_Material)
admin.site.register(Component)
admin.site.register(Item_Type)
admin.site.register(Item)
admin.site.register(Refining_Measure)
admin.site.register(Refining_Recipe)
admin.site.register(Crafting_Measure)
admin.site.register(Crafting_Recipe)
