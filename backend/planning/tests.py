import pytest
from master_data.models import Item, ItemCategory
from inventory.models import StockLocation, StockLedger
from planning.services import check_reorder, moving_average_forecast
from datetime import date


@pytest.mark.django_db
def test_healthy_stock_produces_no_recommendation():
    """If stock is above the reorder point, no recommendation should be created."""
    category = ItemCategory.objects.create(name="Test Category")
    item = Item.objects.create(category=category, sku="TEST-004", name="Test Item", uom="pcs", reorder_point=50, safety_stock=20)
    location = StockLocation.objects.create(name="Test Warehouse", location_type="Warehouse")

    StockLedger.objects.create(item=item, location=location, txn_type='GR', quantity=100, ref_doc_id='00000000-0000-0000-0000-000000000003')

    result = check_reorder(item, location)

    assert result is None


@pytest.mark.django_db
def test_low_stock_produces_explainable_recommendation():
    """If stock is below the reorder point, a recommendation must be
    created WITH a human-readable reason - this is the core
    explainability requirement."""
    category = ItemCategory.objects.create(name="Test Category")
    item = Item.objects.create(category=category, sku="TEST-005", name="Test Item", uom="pcs", reorder_point=50, safety_stock=20)
    location = StockLocation.objects.create(name="Test Warehouse", location_type="Warehouse")

    StockLedger.objects.create(item=item, location=location, txn_type='GR', quantity=30, ref_doc_id='00000000-0000-0000-0000-000000000004')

    result = check_reorder(item, location)

    assert result is not None
    assert result.recommended_qty == 40  # (50 - 30) + 20 safety stock
    assert "30" in result.reason
    assert "50" in result.reason
    assert result.status == 'OPEN'


@pytest.mark.django_db
def test_moving_average_forecast_calculates_correctly():
    """Forecast should be a simple, transparent average - not a black box."""
    category = ItemCategory.objects.create(name="Test Category")
    item = Item.objects.create(category=category, sku="TEST-006", name="Test Item", uom="pcs", reorder_point=10, safety_stock=5)

    forecast = moving_average_forecast(item, [40, 55, 48, 60], date(2026, 1, 1), date(2026, 6, 30))

    assert forecast.forecasted_qty == 50.75
    assert forecast.method == 'MOVING_AVG'