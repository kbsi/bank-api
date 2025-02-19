import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Typography, List, ListItem, ListItemText, Paper, Box, Pagination, IconButton, Dialog, DialogTitle, DialogContent, DialogActions, Button } from '@mui/material';
import Layout from './Layout';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { format, parseISO, isValid } from 'date-fns';

const Logs = () => {
  const [logs, setLogs] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedLog, setSelectedLog] = useState(null);
  const [user, setUser] = useState(null);

  useEffect(() => {
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

    fetchUser();
  }, []);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:5050/api/logs', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
          params: {
            page,
            limit: 30, // Afficher 30 logs par page
          },
        });
        setLogs(response.data.logs.reverse()); // Inverser l'ordre des logs
        setTotalPages(response.data.totalPages);
      } catch (error) {
        console.error('Échec de la récupération des logs', error);
      }
    };

    fetchLogs();
  }, [page]);

  const handlePageChange = (event, value) => {
    setPage(value);
  };

  const handleLogClick = (log) => {
    setSelectedLog(log);
  };

  const handleClose = () => {
    setSelectedLog(null);
  };

  const getLogColor = (level) => {
    switch (level) {
      case 'WARNING':
        return 'orange';
      case 'ERROR':
        return 'red';
      default:
        return 'inherit';
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

  if (!user) {
    return <Typography>Chargement...</Typography>;
  }

  return (
    <Layout user={user} title="Logs">
      <Paper elevation={3} sx={{ padding: 0.5 }}>
        <List>
          {logs.length > 0 ? (
            logs.map((log) => (
              <ListItem key={log._id.$oid} button onClick={() => handleLogClick(log)} sx={{ padding: '1px 2px' }}>
                <ListItemText
                  primary={
                    <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ color: getLogColor(log.level) }}>
                      <span style={{ width: '150px', textAlign: 'left' }}>{log.level}</span>
                      <span style={{ width: '200px', textAlign: 'left' }}>{formatDate(log.timestamp)}</span>
                      <span style={{ flexGrow: 1, textAlign: 'left', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{log.message}</span>
                      <IconButton size="small">
                        <ExpandMoreIcon />
                      </IconButton>
                    </Box>
                  }
                />
              </ListItem>
            ))
          ) : (
            <Typography>Aucun log trouvé.</Typography>
          )}
        </List>
        <Box display="flex" justifyContent="center" mt={1}>
          <Pagination count={totalPages} page={page} onChange={handlePageChange} />
        </Box>
      </Paper>
      <Dialog open={Boolean(selectedLog)} onClose={handleClose}>
        <DialogTitle>Détails du Log</DialogTitle>
        <DialogContent>
          {selectedLog && (
            <>
              <Typography variant="body1"><strong>Niveau :</strong> {selectedLog.level}</Typography>
              <Typography variant="body1"><strong>Date :</strong> {formatDate(selectedLog.timestamp)}</Typography>
              <Typography variant="body1"><strong>Message :</strong> {selectedLog.message}</Typography>
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">Fermer</Button>
        </DialogActions>
      </Dialog>
    </Layout>
  );
};

export default Logs;