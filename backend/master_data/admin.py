from django.contrib import admin
from .models import ItemCategory, Item, Supplier, ItemSupplier

admin.site.register(ItemCategory)
admin.site.register(Item)
admin.site.register(Supplier)
admin.site.register(ItemSupplier)