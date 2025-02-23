import React, { useEffect } from 'react';
import { Container, Typography, Avatar, Tooltip, AppBar, Toolbar, Menu, MenuItem, IconButton } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Layout = ({ user, title, children }) => {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const checkTokenValidity = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          navigate('/login');
          return;
        }
        await axios.get('http://localhost:5050/api/auth/me', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
      } catch (error) {
        console.error('Token invalide ou expiré', error);
        localStorage.removeItem('token');
        navigate('/login');
      }
    };

    checkTokenValidity();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const handleMenuClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleNavigation = (path) => {
    navigate(path);
    handleMenuClose();
  };

  const getInitials = (firstName, lastName) => {
    return `${firstName.charAt(0)}${lastName.charAt(0)}`;
  };

  return (
    <Container component="main" maxWidth="md" sx={{ mt: 4 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            {title}
          </Typography>
          {user && (
            <>
              <Tooltip title={`${user.first_name} ${user.last_name}`}>
                <Avatar sx={{ mr: 2 }}>{user.first_name && user.last_name && getInitials(user.first_name, user.last_name)}</Avatar>
              </Tooltip>
              <IconButton color="inherit" onClick={handleMenuClick}>
                <MenuIcon />
              </IconButton>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
              >
                <MenuItem onClick={() => handleNavigation('/accounts')}>Mes Comptes</MenuItem>
                {user.roles && user.roles.includes('developer') && (
                  <MenuItem onClick={() => handleNavigation('/logs')}>Logs</MenuItem>
                )}
                <MenuItem onClick={handleLogout}>Déconnexion</MenuItem>
              </Menu>
            </>
          )}
        </Toolbar>
      </AppBar>
      {children}
    </Container>
  );
};

export default Layout;