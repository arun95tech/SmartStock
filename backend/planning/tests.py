import pytest
from decimal import Decimal
from datetime import date
from master_data.models import Item, ItemCategory, ItemSupplier, Supplier
from inventory.models import StockLocation, StockLedger
from planning.models import SupplierKPI
from planning.services import (
    check_reorder,
    moving_average_forecast,
    classify_items_abc,
    calculate_supplier_risk,
)


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
    assert result.recommended_qty == 40
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


@pytest.mark.django_db
def test_abc_classification_ranks_by_value():
    """Higher-value items should be classified A before lower-value ones."""
    category = ItemCategory.objects.create(name="Test Category")
    supplier = Supplier.objects.create(name="Test Supplier")

    expensive_item = Item.objects.create(category=category, sku="EXP-001", name="Expensive", uom="pcs", reorder_point=100, safety_stock=10)
    cheap_item = Item.objects.create(category=category, sku="CHP-001", name="Cheap", uom="pcs", reorder_point=100, safety_stock=10)

    ItemSupplier.objects.create(item=expensive_item, supplier=supplier, unit_cost=Decimal('50.00'), lead_time_days=10)
    ItemSupplier.objects.create(item=cheap_item, supplier=supplier, unit_cost=Decimal('0.50'), lead_time_days=10)

    results = classify_items_abc([expensive_item, cheap_item])
    expensive_result = next(r for r in results if r.item == expensive_item)

    assert expensive_result.abc_class == 'A'


@pytest.mark.django_db
def test_supplier_risk_flags_poor_performance_with_reasons():
    """A supplier with bad KPIs should be rated HIGH risk with visible reasons."""
    supplier = Supplier.objects.create(name="Unreliable Supplier")
    kpi = SupplierKPI.objects.create(
        supplier=supplier, period='2026-01-01',
        otif_score=Decimal('70.00'), avg_lead_time=Decimal('30.00'), defect_rate=Decimal('5.00')
    )

    result = calculate_supplier_risk(supplier, kpi)

    assert result.risk_rating == 'HIGH'
    assert 'OTIF' in result.contributing_factors
    assert 'lead time' in result.contributing_factors
    assert 'Defect rate' in result.contributing_factors


@pytest.mark.django_db
def test_supplier_risk_low_when_kpis_are_good():
    """A supplier with good KPIs should be rated LOW risk."""
    supplier = Supplier.objects.create(name="Reliable Supplier")
    kpi = SupplierKPI.objects.create(
        supplier=supplier, period='2026-01-01',
        otif_score=Decimal('98.00'), avg_lead_time=Decimal('7.00'), defect_rate=Decimal('0.50')
    )

    result = calculate_supplier_risk(supplier, kpi)

    assert result.risk_rating == 'LOW'