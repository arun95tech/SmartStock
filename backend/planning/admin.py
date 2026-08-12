from django.contrib import admin
from .models import ForecastRun, ReorderRecommendation, ABCClassificationRun, SupplierKPI, SupplierRiskScore

admin.site.register(ForecastRun)
admin.site.register(ReorderRecommendation)
admin.site.register(ABCClassificationRun)
admin.site.register(SupplierKPI)
admin.site.register(SupplierRiskScore)