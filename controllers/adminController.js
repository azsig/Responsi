const db = require('../config/db');
const { sendCommandToRaspberryPi, notifyClients } = require('./websocket');

exports.showLogin = (req, res) => {
  res.render('login');
};

exports.handleLogin = (req, res) => {
  const { username, password } = req.body;
  if (username === 'admin' && password === 'admin') {
    req.session.isAdmin = true;
    res.redirect('/admin/dashboard');
  } else {
    res.send('Invalid credentials');
  }
};

exports.getDataByIndex = async (req, res) => {
  const index = parseInt(req.params.index, 10); // Ambil indeks dari parameter URL
  try {
    let query;
    let params;

    if (index === 0) {
      // Jika indeks adalah 0, ambil data terbaru
      query = 'SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1';
      params = [];
    } else {
      // Jika indeks lebih besar dari 0, gunakan OFFSET
      query = 'SELECT * FROM sensor_data ORDER BY id ASC OFFSET $1 LIMIT 1';
      params = [index - 1]; // Kurangi 1 karena indeks dimulai dari 0
    }

    const result = await db.query(query, params);
    const data = result.rows[0];

    if (data) {
      res.json(data); // Kirim data dalam format JSON
    } else {
      res.status(404).send('No data found for the given index');
    }
  } catch (error) {
    console.error('Error fetching data by index:', error);
    res.status(500).send('Error fetching data by index');
  }
};

exports.showAdminDashboard = async (req, res) => {
  if (!req.session.isAdmin) {
    return res.redirect('/admin/login');
  }

  try {
    // Fetch the latest data from the database
    const result = await db.query('SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1');
    const data = result.rows[0];

    // Notify all clients with the latest data
    notifyClients();

    // Render the admin dashboard with the fetched data
    res.render('adminDashboard', { data });
  } catch (error) {
    console.error('Error fetching data for admin dashboard:', error);
    res.status(500).send('Error fetching data');
  }
};

exports.handleEmergency = (req, res) => {
  const command = req.body.command; // Example: { command: "activate_actuator" }
  sendCommandToRaspberryPi(command);
  res.send(`Command sent to Raspberry Pi: ${command}`);
};