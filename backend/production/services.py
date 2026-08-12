from inventory.models import StockLedger
from inventory.services import get_current_stock
from .models import MaterialIssue

def issue_material(reservation, location, qty):
    """
    Consumes reserved stock for a Work Order. This is the only place
    that actually writes a negative StockLedger entry for production
    consumption - reserving stock never touches the ledger by itself.
    """
    issue = MaterialIssue.objects.create(
        work_order=reservation.work_order,
        reservation=reservation,
        qty_issued=qty,
    )

    StockLedger.objects.create(
        item=reservation.item,
        location=location,
        txn_type='ISSUE',
        quantity=-qty,
        ref_doc_id=issue.id,
    )

    return issue


def receive_finished_goods(work_order, location, qty, completion_date):
    """
    Completes a Work Order - creates the FGReceipt and posts a
    POSITIVE ledger entry for the parent item (the thing that was made).
    """
    from .models import FGReceipt

    fg = FGReceipt.objects.create(
        work_order=work_order,
        qty_completed=qty,
        completion_date=completion_date,
    )

    StockLedger.objects.create(
        item=work_order.bom.parent_item,
        location=location,
        txn_type='FG',
        quantity=qty,
        ref_doc_id=fg.id,
    )

    work_order.state = 'COMPLETED'
    work_order.save()

    return fg