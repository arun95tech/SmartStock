import pytest
from master_data.models import Item, ItemCategory
from inventory.models import StockLocation, StockLedger
from inventory.services import get_current_stock


@pytest.mark.django_db
def test_stock_balance_is_derived_not_stored():
    """
    Core architectural proof: current stock is calculated fresh from
    the ledger, not stored anywhere. Two entries (+100, -30) should
    sum to 70.
    """
    category = ItemCategory.objects.create(name="Test Category")
    item = Item.objects.create(
        category=category, sku="TEST-001", name="Test Item",
        uom="pcs", reorder_point=10, safety_stock=5
    )
    location = StockLocation.objects.create(name="Test Warehouse", location_type="Warehouse")

    assert get_current_stock(item, location) == 0

    StockLedger.objects.create(item=item, location=location, txn_type='GR', quantity=100, ref_doc_id='00000000-0000-0000-0000-000000000001')
    assert get_current_stock(item, location) == 100

    StockLedger.objects.create(item=item, location=location, txn_type='ISSUE', quantity=-30, ref_doc_id='00000000-0000-0000-0000-000000000002')
    assert get_current_stock(item, location) == 70