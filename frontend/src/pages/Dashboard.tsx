import { Box, Typography, Button } from '@mui/material';
import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
  const { logout } = useAuth();

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h5">Dashboard (placeholder)</Typography>
      <Button onClick={logout} sx={{ mt: 2 }}>Log out</Button>
    </Box>
  );
}