import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Login';
import Accounts from './Accounts';
import AccountTransactions from './AccountTransactions';
import Logs from './Logs';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/accounts" element={<Accounts />} />
        <Route path="/accounts/:accountId/transactions" element={<AccountTransactions />} />
        <Route path="/logs" element={<Logs />} />
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Login />} />
        {/* Ajoutez d'autres routes ici */}
      </Routes>
    </Router>
  );
};

export default App;