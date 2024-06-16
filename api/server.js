const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();

module.exports = app;

app.use(cors());
app.use(express.json());

app.get('/projects', async (req, res) => {
  try {
    const response = await axios.get('http://backend:5002/projects');
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching projects:', error.message);
    res.status(500).json({ error: 'Error fetching projects' });
  }
});

app.get('/co2_by_industry', async (req, res) => {
  try {
    const response = await axios.get('http://backend:5002/co2_by_industry');
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching CO2 by industry:', error.message);
    res.status(500).json({ error: 'Error fetching CO2 by industry' });
  }
});

app.get('/', (req, res) => {
  res.send('API is running.');
});

app.listen(5001, () => {
  console.log('API server is running on port 5001');
});
