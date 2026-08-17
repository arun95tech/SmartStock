import { useEffect, useState } from 'react';
import { Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Chip, Button, CircularProgress, Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { getItems } from '../api/masterData';
import type { Item } from '../api/masterData';
import apiClient from '../api/client';

interface ABCResult {
  item: string;
  abc_class: string;
}

export default function ItemsList() {
  const [items, setItems] = useState<Item[]>([]);
  const [abcMap, setAbcMap] = useState<Record<string, string>>({});
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
      const fetchedItems = await getItems();
      setItems(fetchedItems);

      const abcResponse = await apiClient.post<ABCResult[]>('/planning/abc-runs/run/');
      const map: Record<string, string> = {};
      abcResponse.data.forEach((r) => {
        map[r.item] = r.abc_class;
      });
      setAbcMap(map);
    } catch (err) {
      setError('Failed to load items.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <Box sx={{ p: 4, maxWidth: 900, mx: 'auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h5">Items</Typography>
          <Typography variant="body2" color="text.secondary">{items.length} SKUs</Typography>
        </Box>
        <Button onClick={() => navigate('/dashboard')} variant="outlined" size="small">
          Back to dashboard
        </Button>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {loading ? (
        <CircularProgress />
      ) : (
        <TableContainer component={Paper} elevation={0} sx={{ border: '1px solid #e0e0e0' }}>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>SKU</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Class</TableCell>
                <TableCell align="right">Reorder point</TableCell>
                <TableCell align="right">Safety stock</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {items.map((item) => (
                <TableRow key={item.id}>
                  <TableCell><code>{item.sku}</code></TableCell>
                  <TableCell>{item.name}</TableCell>
                  <TableCell>
                    {abcMap[item.id] && (
                      <Chip label={abcMap[item.id]} size="small" />
                    )}
                  </TableCell>
                  <TableCell align="right">{item.reorder_point}</TableCell>
                  <TableCell align="right">{item.safety_stock}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </Box>
  );
}