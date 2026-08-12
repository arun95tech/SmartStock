from inventory.models import StockLedger, StockLocation
import uuid


def process_gr_line(gr_line, location):
    
    if gr_line.qc_status != 'PASSED':
        return None  # failed or still pending - no stock movement yet

    entry = StockLedger.objects.create(
        item=gr_line.po_line.item,
        location=location,
        txn_type='GR',
        quantity=gr_line.qty_received,
        ref_doc_id=gr_line.gr.id,
    )
    return entry