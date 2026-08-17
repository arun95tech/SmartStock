import { useEffect, useState } from 'react';
import { Box, Typography, Button, Grid, Paper, Alert, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getItems } from '../api/masterData';
import type { Item } from '../api/masterData';
import { getLocations } from '../api/inventory';
import type { StockLocation } from '../api/inventory';
import { checkReorder } from '../api/planning';
import type { ReorderRecommendation } from '../api/planning';

export default function Dashboard() {
  const { logout } = useAuth(); const navigate = useNavigate();
  const [items, setItems] = useState<Item[]>([]);
  const [recommendations, setRecommendations] = useState<ReorderRecommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    setLoading(true);
    setError('');
    try {
      const [fetchedItems, locations] = await Promise.all([getItems(), getLocations()]);
      setItems(fetchedItems);

      if (locations.length === 0) {
        setError('No stock location found. Add one via the admin panel first.');
        return;
      }
      const location: StockLocation = locations[0];

      const results: ReorderRecommendation[] = [];
      for (const item of fetchedItems) {
        const rec = await checkReorder(item.id, location.id);
        if (rec) {
          results.push(rec);
        }
      }
      setRecommendations(results);
    } catch (err) {
      setError('Failed to load dashboard data. Is the backend running?');
    } finally {
      setLoading(false);
    }
  }

  return (
    <Box sx={{ p: 4, maxWidth: 900, mx: 'auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box>
          <Typography variant="h5">Dashboard</Typography>
          <Typography variant="body2" color="text.secondary">BrightBuild Ltd</Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button onClick={logout} variant="outlined" size="small">Log out</Button>
          <Button onClick={() => navigate('/items')} variant="outlined" size="small">Items</Button>
          <Button onClick={() => navigate('/purchase-orders')} variant="outlined" size="small">Purchase orders</Button>
        </Box>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {loading ? (
        <CircularProgress />
      ) : (
        <>
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={6} sm={3}>
              <Paper elevation={0} sx={{ p: 2, bgcolor: '#f5f5f0' }}>
                <Typography variant="caption" color="text.secondary">Total items</Typography>
                <Typography variant="h5">{items.length}</Typography>
              </Paper>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Paper elevation={0} sx={{ p: 2, bgcolor: '#fdf0e0' }}>
                <Typography variant="caption" color="text.secondary">Low stock items</Typography>
                <Typography variant="h5">{recommendations.length}</Typography>
              </Paper>
            </Grid>
          </Grid>

          <Paper elevation={0} sx={{ p: 3, border: '1px solid #e0e0e0' }}>
            <Typography variant="subtitle1" sx={{ mb: 2 }}>Reorder recommendations</Typography>

            {recommendations.length === 0 ? (
              <Typography variant="body2" color="text.secondary">
                All items are above their reorder point. Nothing needs attention right now.
              </Typography>
            ) : (
              recommendations.map((rec) => (
                <Box key={rec.id} sx={{ py: 1.5, borderTop: '1px solid #eee' }}>
                  <Typography variant="body2" sx={{ fontWeight: 500 }}>
                    {rec.reason}
                  </Typography>
                </Box>
              ))
            )}
          </Paper>
        </>
      )}
    </Box>
  );
}