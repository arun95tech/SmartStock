from django.db.models import Sum
from .models import StockLedger


def get_current_stock(item, location=None):
    """
    Current stock is NOT a stored field anywhere.
    It is always calculated fresh from the ledger.
    If location is given, returns stock at that location only.
    Otherwise returns total stock across all locations.
    """
    entries = StockLedger.objects.filter(item=item)
    if location:
        entries = entries.filter(location=location)

    total = entries.aggregate(total=Sum('quantity'))['total']
    return total or 0