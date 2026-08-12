import pytest
from datetime import date
from master_data.models import Item, ItemCategory
from inventory.models import StockLocation
from inventory.services import get_current_stock
from production.models import BOMHeader, BOMLine, WorkOrder, MaterialReservation
from production.services import issue_material, receive_finished_goods


@pytest.mark.django_db
def test_reservation_does_not_move_stock():
    """Reserving material should NOT touch the ledger - only issuing does."""
    category = ItemCategory.objects.create(name="Test Category")
    component = Item.objects.create(category=category, sku="COMP-001", name="Component", uom="pcs", reorder_point=10, safety_stock=5)
    parent = Item.objects.create(category=category, sku="PARENT-001", name="Parent", uom="pcs", reorder_point=5, safety_stock=2)
    location = StockLocation.objects.create(name="Test Warehouse", location_type="Warehouse")

    from inventory.models import StockLedger
    StockLedger.objects.create(item=component, location=location, txn_type='GR', quantity=100, ref_doc_id='00000000-0000-0000-0000-000000000005')

    bom = BOMHeader.objects.create(parent_item=parent, version='1.0', active=True)
    BOMLine.objects.create(bom=bom, component_item=component, qty_per_unit=4)
    wo = WorkOrder.objects.create(bom=bom, qty_planned=5, state='RELEASED', due_date=date.today())

    MaterialReservation.objects.create(work_order=wo, item=component, qty_reserved=20)

    assert get_current_stock(component, location) == 100  # unchanged


@pytest.mark.django_db
def test_full_production_chain_moves_stock_correctly():
    """Issue should decrease component stock; FG receipt should increase
    parent stock and mark the work order COMPLETED."""
    category = ItemCategory.objects.create(name="Test Category")
    component = Item.objects.create(category=category, sku="COMP-002", name="Component", uom="pcs", reorder_point=10, safety_stock=5)
    parent = Item.objects.create(category=category, sku="PARENT-002", name="Parent", uom="pcs", reorder_point=5, safety_stock=2)
    location = StockLocation.objects.create(name="Test Warehouse", location_type="Warehouse")

    from inventory.models import StockLedger
    StockLedger.objects.create(item=component, location=location, txn_type='GR', quantity=100, ref_doc_id='00000000-0000-0000-0000-000000000006')

    bom = BOMHeader.objects.create(parent_item=parent, version='1.0', active=True)
    BOMLine.objects.create(bom=bom, component_item=component, qty_per_unit=4)
    wo = WorkOrder.objects.create(bom=bom, qty_planned=5, state='IN_PROGRESS', due_date=date.today())
    reservation = MaterialReservation.objects.create(work_order=wo, item=component, qty_reserved=20)

    issue_material(reservation, location, 20)
    assert get_current_stock(component, location) == 80  # 100 - 20

    receive_finished_goods(wo, location, 5, date.today())
    assert get_current_stock(parent, location) == 5

    wo.refresh_from_db()
    assert wo.state == 'COMPLETED'