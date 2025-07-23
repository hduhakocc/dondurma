import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../auth/AuthContext';
import { Container, Typography, Table, TableHead, TableRow, TableCell, TableBody, Paper } from '@mui/material';

export default function Products() {
  const { token } = useAuth();
  const [products, setProducts] = useState([]);

  useEffect(() => {
    axios.get('/api/products', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setProducts(res.data));
  }, [token]);

  return (
    <Container>
      <Typography variant="h4" sx={{ my: 3 }}>Ürünler</Typography>
      <Paper>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Ad</TableCell>
              <TableCell>Fiyat</TableCell>
              <TableCell>Stok</TableCell>
              <TableCell>Barkod</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {products.map(p => (
              <TableRow key={p.id}>
                <TableCell>{p.name}</TableCell>
                <TableCell>₺{p.price}</TableCell>
                <TableCell>{p.stock}</TableCell>
                <TableCell>{p.barcode}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>
    </Container>
  );
}
