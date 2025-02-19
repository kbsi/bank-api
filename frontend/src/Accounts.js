import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Typography, List, ListItem, ListItemText, Paper, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import Layout from './Layout';

const Accounts = () => {
  const [accounts, setAccounts] = useState([]);
  const [user, setUser] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAccounts = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:5050/api/accounts/my-accounts', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setAccounts(response.data);
      } catch (error) {
        console.error('Échec de la récupération des comptes', error);
      }
    };

    const fetchUser = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:5050/api/auth/me', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUser(response.data);
      } catch (error) {
        console.error('Échec de la récupération de l\'utilisateur', error);
      }
    };

    fetchAccounts();
    fetchUser();
  }, []);

  const handleAccountClick = (accountId) => {
    navigate(`/accounts/${accountId}/transactions`);
  };

  const totalBalance = accounts.reduce((acc, account) => acc + account.balance, 0);

  const currencySymbol = (currency) => {
    switch (currency) {
      case 'USD':
        return '$';
      case 'EUR':
        return '€';
      default:
        return currency;
    }
  };

  return (
    <Layout user={user} title="Mes Comptes">
      <Paper elevation={3} sx={{ padding: 2 }}>
        <Typography component="h2" variant="h6" align="center" gutterBottom>
          Solde Total : {currencySymbol('USD')}{totalBalance}
        </Typography>
        <List>
          {accounts.map((account) => (
            <ListItem key={account._id.$oid} divider button onClick={() => handleAccountClick(account._id.$oid)} sx={{ cursor: 'pointer' }}>
              <ListItemText
                primary={`Numéro de Compte : ${account.account_number}`}
              />
              <Typography
                variant="body2"
                color={account.balance >= 0 ? 'green' : 'red'}
              >
                {account.balance} {currencySymbol(account.currency)}
              </Typography>
            </ListItem>
          ))}
        </List>
      </Paper>
    </Layout>
  );
};

export default Accounts;