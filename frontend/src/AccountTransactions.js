import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Typography, List, ListItem, ListItemText, Paper, Box } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import Layout from './Layout';
import { format, parseISO, isValid } from 'date-fns';

const AccountTransactions = () => {
  const { accountId } = useParams();
  const [transactions, setTransactions] = useState([]);
  const [account, setAccount] = useState(null);
  const [user, setUser] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`http://localhost:5050/api/accounts/${accountId}/transactions`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          params: {
            start_date: new Date(new Date().setDate(new Date().getDate() - 60)).toISOString(),
          },
        });
        setTransactions(response.data);
      } catch (error) {
        console.error('Échec de la récupération des transactions', error);
      }
    };

    const fetchAccount = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`http://localhost:5050/api/accounts/${accountId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setAccount(response.data);
      } catch (error) {
        console.error('Échec de la récupération du compte', error);
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

    fetchTransactions();
    fetchAccount();
    fetchUser();
  }, [accountId]);

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

  const formatDate = (dateString) => {
    if (typeof dateString === 'string') {
      const date = parseISO(dateString);
      if (isValid(date)) {
        return format(date, 'yyyy-MM-dd HH:mm:ss');
      }
    } else if (typeof dateString === 'object' && dateString.$date) {
      const date = new Date(dateString.$date);
      if (isValid(date)) {
        return format(date, 'yyyy-MM-dd HH:mm:ss');
      }
    }
    return 'Date Invalide';
  };

  if (!account) {
    return <Typography>Chargement...</Typography>;
  }

  return (
    <Layout user={user} title={`Transactions du Compte : ${account.account_number}`}>
      <Paper elevation={3} sx={{ padding: 2 }}>
        <Typography
          component="h2"
          variant="h6"
          align="center"
          gutterBottom
          sx={{ color: account.balance >= 0 ? 'green' : 'red' }}
        >
          Solde : {account.balance} {currencySymbol(account.currency)}
        </Typography>
        <List>
          {transactions.length > 0 ? (
            transactions.map((transaction) => (
              <ListItem key={transaction._id}>
                <ListItemText
                  primary={
                    <Box display="flex" justifyContent="space-between">
                      <span>{formatDate(transaction.timestamp)}</span>
                      <span>{transaction.type}</span>
                      <span style={{ color: transaction.amount >= 0 ? 'green' : 'red' }}>
                        {transaction.amount} {currencySymbol(transaction.currency)}
                      </span>
                    </Box>
                  }
                />
              </ListItem>
            ))
          ) : (
            <Typography>Aucune transaction trouvée pour ce compte.</Typography>
          )}
        </List>
      </Paper>
    </Layout>
  );
};

export default AccountTransactions;