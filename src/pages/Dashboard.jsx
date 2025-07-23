import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../auth/AuthContext';
import { Container, Typography, Grid, Paper } from '@mui/material';

export default function Dashboard() {
  const { token } = useAuth();
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get('/api/dashboard', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setData(res.data));
  }, [token]);

  if (!data) return <div>Yükleniyor...</div>;

  return (
    <Container>
      <Typography variant="h4" sx={{ my: 3 }}>Dashboard</Typography>
      <Grid container spacing={2}>
        <Grid item xs={6} md={3}><Paper sx={{ p: 2 }}>Sipariş: {data.order_count}</Paper></Grid>
        <Grid item xs={6} md={3}><Paper sx={{ p: 2 }}>Ciro: ₺{data.total_revenue}</Paper></Grid>
        <Grid item xs={6} md={3}><Paper sx={{ p: 2 }}>Teslim Edilen: {data.delivered_count}</Paper></Grid>
        <Grid item xs={6} md={3}><Paper sx={{ p: 2 }}>Bekleyen: {data.pending_count}</Paper></Grid>
      </Grid>
      <Typography variant="h6" sx={{ mt: 4 }}>Düşük Stoklar</Typography>
      {data.low_stock.length === 0 ? <div>Yok</div> : (
        <ul>
          {data.low_stock.map(p => <li key={p.id}>{p.name} (Stok: {p.stock})</li>)}
        </ul>
      )}
    </Container>
  );
}
