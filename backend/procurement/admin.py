from django.contrib import admin
from .models import PurchaseOrder, POLine, GoodsReceipt, GRLine, QCHold

admin.site.register(PurchaseOrder)
admin.site.register(POLine)
admin.site.register(GoodsReceipt)
admin.site.register(GRLine)
admin.site.register(QCHold)