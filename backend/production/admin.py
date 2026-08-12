from django.contrib import admin
from .models import BOMHeader, BOMLine, WorkOrder, MaterialReservation, MaterialIssue, FGReceipt

admin.site.register(BOMHeader)
admin.site.register(BOMLine)
admin.site.register(WorkOrder)
admin.site.register(MaterialReservation)
admin.site.register(MaterialIssue)
admin.site.register(FGReceipt)