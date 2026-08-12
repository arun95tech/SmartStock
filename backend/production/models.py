import uuid
from django.db import models
from master_data.models import Item



class BOMHeader(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='boms')
    version = models.CharField(max_length=20, default='1.0')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"BOM for {self.parent_item.sku} (v{self.version})"


# One component line within a BOM
class BOMLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bom = models.ForeignKey(BOMHeader, on_delete=models.CASCADE, related_name='lines')
    component_item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='used_in_boms')
    qty_per_unit = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f"{self.qty_per_unit} x {self.component_item.sku}"



# state moves through: DRAFT -> RELEASED -> IN_PROGRESS -> COMPLETED
class WorkOrder(models.Model):
    STATE_CHOICES = [
        ('DRAFT', 'Draft'),
        ('RELEASED', 'Released'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bom = models.ForeignKey(BOMHeader, on_delete=models.PROTECT, related_name='work_orders')
    qty_planned = models.IntegerField()
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='DRAFT')
    due_date = models.DateField()

    def __str__(self):
        return f"WO-{str(self.id)[:8]} ({self.state})"


# Earmarks stock for a Work Order without moving it yet.
class MaterialReservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='reservations')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='reservations')
    qty_reserved = models.IntegerField()

    def __str__(self):
        return f"{self.item.sku} x {self.qty_reserved} reserved for {self.work_order}"


class MaterialIssue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.PROTECT, related_name='issues')
    reservation = models.ForeignKey(MaterialReservation, on_delete=models.PROTECT, related_name='issues')
    qty_issued = models.IntegerField()
    issue_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Issued {self.qty_issued} for {self.work_order}"


# Records completed finished goods coming out of a Work Order.
class FGReceipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_order = models.OneToOneField(WorkOrder, on_delete=models.PROTECT, related_name='fg_receipt')
    qty_completed = models.IntegerField()
    completion_date = models.DateField()

    def __str__(self):
        return f"{self.qty_completed} completed for {self.work_order}"