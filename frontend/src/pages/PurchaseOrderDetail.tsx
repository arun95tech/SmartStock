import { useEffect, useState } from 'react';
import { Box, Typography, Paper, Chip, Button, CircularProgress, Alert, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';
import { useNavigate } from 'react-router-dom';
import { getPurchaseOrders, getGoodsReceipts, getGRLines, getQCHolds } from '../api/procurement';
import type { PurchaseOrder, GoodsReceipt, GRLine, QCHold } from '../api/procurement';

export default function PurchaseOrderDetail() {
  const [po, setPo] = useState<PurchaseOrder | null>(null);
  const [grLines, setGrLines] = useState<GRLine[]>([]);
  const [holds, setHolds] = useState<QCHold[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    setLoading(true);
    setError('');
    try {
      const [pos, receipts, lines, qcHolds] = await Promise.all([
        getPurchaseOrders(),
        getGoodsReceipts(),
        getGRLines(),
        getQCHolds(),
      ]);

      if (pos.length === 0) {
        setError('No purchase orders found.');
        return;
      }
      const firstPo = pos[0];
      setPo(firstPo);

      const relatedReceipts = receipts.filter((r: GoodsReceipt) => r.po === firstPo.id);
      const receiptIds = relatedReceipts.map((r) => r.id);
      const relatedLines = lines.filter((l: GRLine) => receiptIds.includes(l.gr));
      setGrLines(relatedLines);

      const lineIds = relatedLines.map((l) => l.id);
      const relatedHolds = qcHolds.filter((h: QCHold) => lineIds.includes(h.gr_line));
      setHolds(relatedHolds);
    } catch (err) {
      setError('Failed to load purchase order data.');
    } finally {
      setLoading(false);
    }
  }

  function holdForLine(lineId: string): QCHold | undefined {
    return holds.find((h) => h.gr_line === lineId);
  }

  return (
    <Box sx={{ p: 4, maxWidth: 700, mx: 'auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5">Purchase order</Typography>
        <Button onClick={() => navigate('/dashboard')} variant="outlined" size="small">
          Back to dashboard
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {loading ? (
        <CircularProgress />
      ) : po ? (
        <Paper elevation={0} sx={{ p: 3, border: '1px solid #e0e0e0' }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="subtitle1">PO-{po.id.slice(0, 8)}</Typography>
            <Chip label={po.status} size="small" color={po.status === 'APPROVED' ? 'success' : 'default'} />
          </Box>

          <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
            Ordered {po.order_date} — expected {po.expected_date}
          </Typography>

          <Typography variant="subtitle2" sx={{ mb: 1 }}>Goods receipt lines</Typography>
          <List dense>
            {grLines.map((line) => {
              const hold = holdForLine(line.id);
              return (
                <ListItem key={line.id} divider>
                  <ListItemIcon>
                    {line.qc_status === 'PASSED' ? (
                      <CheckCircleIcon color="success" fontSize="small" />
                    ) : (
                      <WarningIcon color="error" fontSize="small" />
                    )}
                  </ListItemIcon>
                  <ListItemText
                    primary={`${line.qty_received} units received`}
                    secondary={
                      line.qc_status === 'PASSED'
                        ? 'QC passed — added to stock'
                        : hold
                        ? `QC hold: ${hold.hold_reason}`
                        : 'QC pending'
                    }
                  />
                </ListItem>
              );
            })}
          </List>
        </Paper>
      ) : null}
    </Box>
  );
}