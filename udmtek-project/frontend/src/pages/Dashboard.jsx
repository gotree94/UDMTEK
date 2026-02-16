import React, { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Box,
  Chip,
  LinearProgress,
  Alert,
} from '@mui/material';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import {
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Speed as SpeedIcon,
  Memory as MemoryIcon,
  Timeline as TimelineIcon,
} from '@mui/icons-material';

import { fetchDashboardData } from '../services/api';

const COLORS = ['#00C49F', '#FFBB28', '#FF8042', '#0088FE'];

function Dashboard({ realtimeData }) {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
    const interval = setInterval(loadDashboardData, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      const data = await fetchDashboardData();
      setDashboardData(data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <LinearProgress />;
  }

  const systemStats = dashboardData?.system_stats || {
    total_plcs: 12,
    active_plcs: 10,
    critical_alerts: 2,
    pending_maintenance: 5,
    avg_health_score: 78.5,
  };

  const faultsByCategory = dashboardData?.faults_by_category || [
    { name: 'Hardware', value: 15 },
    { name: 'Software', value: 8 },
    { name: 'Communication', value: 5 },
    { name: 'Process', value: 12 },
  ];

  const healthTrend = dashboardData?.health_trend || [
    { time: '00:00', score: 82 },
    { time: '04:00', score: 80 },
    { time: '08:00', score: 78 },
    { time: '12:00', score: 76 },
    { time: '16:00', score: 79 },
    { time: '20:00', score: 81 },
  ];

  const maintenanceSchedule = dashboardData?.upcoming_maintenance || [
    { equipment: 'Motor-001', days: 3, priority: 'HIGH' },
    { equipment: 'Pump-005', days: 7, priority: 'MEDIUM' },
    { equipment: 'Valve-012', days: 14, priority: 'LOW' },
  ];

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard Overview
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Active PLCs
                  </Typography>
                  <Typography variant="h4">
                    {systemStats.active_plcs}/{systemStats.total_plcs}
                  </Typography>
                </Box>
                <MemoryIcon sx={{ fontSize: 48, color: 'primary.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Critical Alerts
                  </Typography>
                  <Typography variant="h4" color="error">
                    {systemStats.critical_alerts}
                  </Typography>
                </Box>
                <ErrorIcon sx={{ fontSize: 48, color: 'error.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Pending Maintenance
                  </Typography>
                  <Typography variant="h4" color="warning.main">
                    {systemStats.pending_maintenance}
                  </Typography>
                </Box>
                <WarningIcon sx={{ fontSize: 48, color: 'warning.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Avg Health Score
                  </Typography>
                  <Typography variant="h4" color="success.main">
                    {systemStats.avg_health_score}%
                  </Typography>
                </Box>
                <SpeedIcon sx={{ fontSize: 48, color: 'success.main' }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts Row */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {/* Health Trend Chart */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              System Health Trend (24h)
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={healthTrend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="score" 
                  stroke="#2196f3" 
                  strokeWidth={2}
                  name="Health Score (%)"
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Faults by Category */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Faults by Category
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={faultsByCategory}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {faultsByCategory.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Alerts and Maintenance */}
      <Grid container spacing={3}>
        {/* Recent Alerts */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Alerts
            </Typography>
            <Box>
              <Alert severity="error" sx={{ mb: 1 }}>
                <Typography variant="body2">
                  <strong>MOTOR-003:</strong> Communication timeout detected
                </Typography>
              </Alert>
              <Alert severity="error" sx={{ mb: 1 }}>
                <Typography variant="body2">
                  <strong>PUMP-007:</strong> Overload condition - immediate attention required
                </Typography>
              </Alert>
              <Alert severity="warning" sx={{ mb: 1 }}>
                <Typography variant="body2">
                  <strong>SENSOR-015:</strong> Value out of range
                </Typography>
              </Alert>
              <Alert severity="info">
                <Typography variant="body2">
                  <strong>VALVE-022:</strong> Scheduled maintenance due in 5 days
                </Typography>
              </Alert>
            </Box>
          </Paper>
        </Grid>

        {/* Upcoming Maintenance */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Upcoming Maintenance
            </Typography>
            <Box>
              {maintenanceSchedule.map((item, index) => (
                <Box 
                  key={index}
                  sx={{ 
                    display: 'flex', 
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    mb: 2,
                    p: 1.5,
                    bgcolor: 'background.default',
                    borderRadius: 1
                  }}
                >
                  <Box>
                    <Typography variant="body1" fontWeight="medium">
                      {item.equipment}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Due in {item.days} days
                    </Typography>
                  </Box>
                  <Chip 
                    label={item.priority}
                    color={
                      item.priority === 'HIGH' ? 'error' : 
                      item.priority === 'MEDIUM' ? 'warning' : 
                      'default'
                    }
                    size="small"
                  />
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Real-time Data Display */}
      {realtimeData && (
        <Box sx={{ mt: 3 }}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Real-time Data Stream
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {JSON.stringify(realtimeData, null, 2)}
            </Typography>
          </Paper>
        </Box>
      )}
    </Box>
  );
}

export default Dashboard;
