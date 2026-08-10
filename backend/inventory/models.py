import uuid
from django.db import models
from master_data.models import Item


# A physical place stock can sit — a warehouse, a shelf, a QC hold area
class StockLocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    location_type = models.CharField(max_length=50)  # e.g. "Warehouse", "QC Hold"

    def __str__(self):
        return self.name



class StockLedger(models.Model):
    TXN_TYPES = [
        ('GR', 'Goods Receipt'),
        ('ISSUE', 'Material Issue'),
        ('FG', 'Finished Goods Receipt'),
        ('ADJUST', 'Stock Adjustment'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='ledger_entries')
    location = models.ForeignKey(StockLocation, on_delete=models.PROTECT, related_name='ledger_entries')
    txn_type = models.CharField(max_length=10, choices=TXN_TYPES)
    quantity = models.IntegerField()  # positive = stock in, negative = stock out
    ref_doc_id = models.UUIDField()  # points to the PO/GR/WO/Adjustment that caused this
    txn_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.sku} | {self.txn_type} | {self.quantity}"


# Manual correction to stock — damaged goods, cycle count fix, returns.
# This is not a shortcut around the ledger — approving one of these
class StockAdjustment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='adjustments')
    location = models.ForeignKey(StockLocation, on_delete=models.PROTECT, related_name='adjustments')
    qty_delta = models.IntegerField()  # + or - depending on the correction
    reason = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.item.sku} adjust {self.qty_delta} ({self.reason})"