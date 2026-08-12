from decimal import Decimal
from .models import ForecastRun, ReorderRecommendation
from inventory.services import get_current_stock


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
        return None  # stock is fine, no recommendation needed

    shortfall = item.reorder_point - current_stock
    # recommend enough to get back above reorder point, plus safety stock
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