from decimal import Decimal
from .models import ForecastRun, ReorderRecommendation, ABCClassificationRun, SupplierRiskScore
from inventory.services import get_current_stock
from master_data.models import Item, ItemSupplier


def moving_average_forecast(item, past_demand, period_start, period_end):
    if not past_demand:
        avg = Decimal('0')
    else:
        avg = Decimal(sum(past_demand)) / Decimal(len(past_demand))

    run = ForecastRun.objects.create(
        item=item,
        method='MOVING_AVG',
        period_start=period_start,
        period_end=period_end,
        forecasted_qty=avg,
    )
    return run


def check_reorder(item, location):
    current_stock = get_current_stock(item, location)

    if current_stock >= item.reorder_point:
        return None

    shortfall = item.reorder_point - current_stock
    recommended_qty = shortfall + item.safety_stock

    reason = (
        f"Current stock ({current_stock}) is below reorder point "
        f"({item.reorder_point}). Recommending {recommended_qty} units "
        f"to restore safety stock buffer of {item.safety_stock}."
    )

    recommendation = ReorderRecommendation.objects.create(
        item=item,
        current_stock=current_stock,
        reorder_point=item.reorder_point,
        recommended_qty=recommended_qty,
        reason=reason,
        status='OPEN',
    )
    return recommendation


def classify_items_abc(items=None):
    if items is None:
        items = Item.objects.all()

    item_values = []
    for item in items:
        item_supplier = ItemSupplier.objects.filter(item=item).first()
        unit_cost = item_supplier.unit_cost if item_supplier else Decimal('0')
        annual_value = unit_cost * item.reorder_point
        item_values.append((item, annual_value))

    item_values.sort(key=lambda pair: pair[1], reverse=True)

    total_value = sum(value for _, value in item_values) or Decimal('1')

    results = []
    running_total = Decimal('0')
    for item, value in item_values:
        cumulative_before = running_total / total_value
        running_total += value

        if cumulative_before < Decimal('0.8'):
            abc_class = 'A'
        elif cumulative_before < Decimal('0.95'):
            abc_class = 'B'
        else:
            abc_class = 'C'

        run = ABCClassificationRun.objects.create(
            item=item,
            abc_class=abc_class,
            annual_value=value,
        )
        results.append(run)

    return results


def calculate_supplier_risk(supplier, kpi):
    factors = []
    risk_points = 0

    if kpi.otif_score < 85:
        risk_points += 2
        factors.append(f"OTIF score {kpi.otif_score}% is below 85% threshold")

    if kpi.avg_lead_time > 21:
        risk_points += 1
        factors.append(f"Average lead time {kpi.avg_lead_time} days exceeds 21 day threshold")

    if kpi.defect_rate > 2:
        risk_points += 2
        factors.append(f"Defect rate {kpi.defect_rate}% exceeds 2% threshold")

    if risk_points >= 4:
        rating = 'HIGH'
    elif risk_points >= 2:
        rating = 'MEDIUM'
    else:
        rating = 'LOW'

    if not factors:
        factors.append("All KPIs within acceptable thresholds")

    score = SupplierRiskScore.objects.create(
        supplier=supplier,
        risk_rating=rating,
        contributing_factors="; ".join(factors),
    )
    return score
