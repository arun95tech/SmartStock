from django.contrib import admin
from .models import StockLocation, StockLedger, StockAdjustment

admin.site.register(StockLocation)
admin.site.register(StockLedger)
admin.site.register(StockAdjustment)