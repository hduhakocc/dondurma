import React, { useState } from 'react';
import { useAuth } from '../auth/AuthContext';
import { TextField, Button, Container, Typography, Box } from '@mui/material';

export default function Login() {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const ok = await login(username, password);
    if (!ok) setError('Giriş başarısız!');
  };

  return (
    <Container maxWidth="xs">
      <Box mt={10}>
        <Typography variant="h5" align="center">Giriş Yap</Typography>
        <form onSubmit={handleSubmit}>
          <TextField label="Kullanıcı Adı" fullWidth margin="normal" value={username} onChange={e => setUsername(e.target.value)} />
          <TextField label="Şifre" type="password" fullWidth margin="normal" value={password} onChange={e => setPassword(e.target.value)} />
          {error && <Typography color="error">{error}</Typography>}
          <Button type="submit" variant="contained" fullWidth sx={{ mt: 2 }}>Giriş</Button>
        </form>
      </Box>
    </Container>
  );
}
