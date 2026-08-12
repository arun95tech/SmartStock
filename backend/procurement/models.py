import uuid
from django.db import models
from master_data.models import Item, Supplier


# An order placed with a supplier for one or more items
class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('APPROVED', 'Approved'),
        ('CLOSED', 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    order_date = models.DateField()
    expected_date = models.DateField()

    def __str__(self):
        return f"PO-{str(self.id)[:8]} ({self.supplier.name})"


class POLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='lines')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='po_lines')
    qty_ordered = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item.sku} x {self.qty_ordered}"


# Records that goods physically arrived against a Purchase Order.
# Creating a GoodsReceipt does NOT change stock by itself -
# stock only changes once a GR_Line passes inspection
class GoodsReceipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    po = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT, related_name='goods_receipts')
    received_date = models.DateField()

    def __str__(self):
        return f"GR-{str(self.id)[:8]} for {self.po}"


# One line of a Goods Receipt - what was actually received against one PO line
class GRLine(models.Model):
    QC_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PASSED', 'Passed'),
        ('FAILED', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gr = models.ForeignKey(GoodsReceipt, on_delete=models.CASCADE, related_name='lines')
    po_line = models.ForeignKey(POLine, on_delete=models.PROTECT, related_name='gr_lines')
    qty_received = models.IntegerField()
    qc_status = models.CharField(max_length=10, choices=QC_STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.po_line.item.sku} received {self.qty_received}"


# Created only when a GRLine fails inspection. Holds the failed stock
# until someone decides what to do with it. This is separate from
# GRLine.qc_status - qc_status is set once and never changes, but a
# QCHold has its own lifecycle (state) that moves through several steps.
class QCHold(models.Model):
    STATE_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gr_line = models.OneToOneField(GRLine, on_delete=models.CASCADE, related_name='qc_hold')
    hold_reason = models.CharField(max_length=255)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='PENDING')

    def __str__(self):
        return f"Hold on {self.gr_line} - {self.state}"