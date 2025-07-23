import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../auth/AuthContext';
import { Container, Typography, Table, TableHead, TableRow, TableCell, TableBody, Paper } from '@mui/material';

export default function Customers() {
  const { token } = useAuth();
  const [customers, setCustomers] = useState([]);

  useEffect(() => {
    axios.get('/api/customers', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setCustomers(res.data));
  }, [token]);

  return (
    <Container>
      <Typography variant="h4" sx={{ my: 3 }}>Müşteriler</Typography>
      <Paper>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Ad</TableCell>
              <TableCell>Soyad</TableCell>
              <TableCell>Telefon</TableCell>
              <TableCell>Adres</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {customers.map(c => (
              <TableRow key={c.id}>
                <TableCell>{c.name}</TableCell>
                <TableCell>{c.surname}</TableCell>
                <TableCell>{c.phone}</TableCell>
                <TableCell>{c.address}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>
    </Container>
  );
}
