import uuid
from django.db import models



# abc_class will later be set by the ABC classification logic (Planning app)
class ItemCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    abc_class = models.CharField(max_length=1, blank=True)  # A, B or C

    def __str__(self):
        return self.name


# A single stock keeping unit (SKU)
class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(ItemCategory, on_delete=models.PROTECT, related_name='items')
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    uom = models.CharField(max_length=20)  # unit of measure, e.g. "kg", "pcs"
    reorder_point = models.IntegerField(default=0)
    safety_stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.sku} - {self.name}"


# A company that supplies items to us
class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    risk_rating = models.CharField(max_length=20, blank=True)  # Low, Medium, High
    otif_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


# Links an Item to a Supplier, with cost and lead time specific to that pair
# (one item can have several suppliers, one supplier can supply several items)
class ItemSupplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_suppliers')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='item_suppliers')
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    lead_time_days = models.IntegerField()

    class Meta:
        unique_together = ('item', 'supplier')