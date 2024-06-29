const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();

module.exports = app;

app.use(cors());
app.use(express.json());

const backendUrl = process.env.BACKEND_URL || 'http://backend-discovery.carbon-project-rater-namespace:5002';

app.get('/api/projects', async (req, res) => {
  try {
    const response = await axios.get(`${backendUrl}/projects`);
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching projects:', error.message);
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
      console.error('Response headers:', error.response.headers);
    }
    res.status(500).json({ error: 'Error fetching projects' });
  }
});

app.get('/api/co2_by_industry', async (req, res) => {
  try {
    const response = await axios.get(`${backendUrl}/co2_by_industry`);
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching CO2 by industry:', error.message);
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
      console.error('Response headers:', error.response.headers);
    }
    res.status(500).json({ error: 'Error fetching CO2 by industry' });
  }
});

app.get('/', (req, res) => {
  res.send('API is running.');
});

// Add health check endpoint
app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

app.listen(5001, () => {
  console.log('API server is running on port 5001');
});
