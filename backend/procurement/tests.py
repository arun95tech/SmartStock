import pytest
import uuid
from datetime import date
from master_data.models import Item, ItemCategory, Supplier
from inventory.models import StockLocation
from inventory.services import get_current_stock
from procurement.models import PurchaseOrder, POLine, GoodsReceipt, GRLine
from procurement.services import process_gr_line


@pytest.mark.django_db
def test_passed_qc_posts_to_ledger():
    """A GR line that PASSES QC should create a stock ledger entry."""
    category = ItemCategory.objects.create(name="Test Category")
    item = Item.objects.create(category=category, sku="TEST-002", name="Test Item", uom="pcs", reorder_point=10, safety_stock=5)
    supplier = Supplier.objects.create(name="Test Supplier")
    location = StockLocation.objects.create(name="Test Warehouse", location_type="Warehouse")

    po = PurchaseOrder.objects.create(supplier=supplier, status='APPROVED', order_date=date.today(), expected_date=date.today())
    po_line = POLine.objects.create(po=po, item=item, qty_ordered=100, unit_cost=1.00)
    gr = GoodsReceipt.objects.create(po=po, received_date=date.today())
    gr_line = GRLine.objects.create(gr=gr, po_line=po_line, qty_received=100, qc_status='PASSED')

    entry = process_gr_line(gr_line, location)

    assert entry is not None
    assert get_current_stock(item, location) == 100


@pytest.mark.django_db
def test_failed_qc_does_not_post_to_ledger():
    """A GR line that FAILS QC should NOT move stock at all."""
    category = ItemCategory.objects.create(name="Test Category")
    item = Item.objects.create(category=category, sku="TEST-003", name="Test Item", uom="pcs", reorder_point=10, safety_stock=5)
    supplier = Supplier.objects.create(name="Test Supplier")
    location = StockLocation.objects.create(name="Test Warehouse", location_type="Warehouse")

    po = PurchaseOrder.objects.create(supplier=supplier, status='APPROVED', order_date=date.today(), expected_date=date.today())
    po_line = POLine.objects.create(po=po, item=item, qty_ordered=100, unit_cost=1.00)
    gr = GoodsReceipt.objects.create(po=po, received_date=date.today())
    gr_line = GRLine.objects.create(gr=gr, po_line=po_line, qty_received=100, qc_status='FAILED')

    entry = process_gr_line(gr_line, location)

    assert entry is None
    assert get_current_stock(item, location) == 0