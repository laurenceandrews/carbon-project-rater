const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();

module.exports = app;

app.use(cors());
app.use(express.json());

app.get('/projects', async (req, res) => {
  try {
    // Use the Docker Compose service name `backend` and the internal port
    const response = await axios.get('http://backend:5000/projects');
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching projects' });
  }
});

app.get('/', (req, res) => {
  res.send('API is running.');
});

app.listen(5001, () => {
  console.log('API server is running on port 5001');
});