import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';

// Components
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import PLCParser from './pages/PLCParser';
import UDMLViewer from './pages/UDMLViewer';
import AIAnalysis from './pages/AIAnalysis';
import MaintenanceSchedule from './pages/MaintenanceSchedule';
import RealTimeMonitoring from './pages/RealTimeMonitoring';
import Settings from './pages/Settings';

// Services
import { connectWebSocket, disconnectWebSocket } from './services/websocket';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#ff9800',
    },
    background: {
      default: '#0a1929',
      paper: '#132f4c',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 500,
    },
  },
});

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [realtimeData, setRealtimeData] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');

  useEffect(() => {
    // Connect to WebSocket for real-time data
    const handleMessage = (data) => {
      setRealtimeData(data);
    };

    const handleConnect = () => {
      setConnectionStatus('connected');
      console.log('✅ WebSocket connected');
    };

    const handleDisconnect = () => {
      setConnectionStatus('disconnected');
      console.log('❌ WebSocket disconnected');
    };

    connectWebSocket(handleMessage, handleConnect, handleDisconnect);

    return () => {
      disconnectWebSocket();
    };
  }, []);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', minHeight: '100vh' }}>
          <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
          
          <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
            <Header 
              onMenuClick={toggleSidebar}
              connectionStatus={connectionStatus}
            />
            
            <Box 
              component="main" 
              sx={{ 
                flexGrow: 1, 
                p: 3,
                mt: 8,
                ml: sidebarOpen ? '240px' : 0,
                transition: 'margin 0.3s',
              }}
            >
              <Routes>
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route 
                  path="/dashboard" 
                  element={<Dashboard realtimeData={realtimeData} />} 
                />
                <Route path="/parser" element={<PLCParser />} />
                <Route path="/udml" element={<UDMLViewer />} />
                <Route path="/analysis" element={<AIAnalysis />} />
                <Route path="/maintenance" element={<MaintenanceSchedule />} />
                <Route 
                  path="/monitoring" 
                  element={<RealTimeMonitoring realtimeData={realtimeData} />} 
                />
                <Route path="/settings" element={<Settings />} />
              </Routes>
            </Box>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
