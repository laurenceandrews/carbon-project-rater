const express = require('express');
const axios = require('axios');
const cors = require('cors');

const app = express();

module.exports = app;

app.use(cors());
app.use(express.json());

app.get('/projects', async (req, res) => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/projects');
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching projects' });
  }
});

app.listen(5001, () => {
  console.log('Server is running on port 5001');
});