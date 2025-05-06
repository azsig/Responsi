const passport = require('passport');
const bcrypt = require('bcryptjs');
const db = require('../config/db');
const { sendCommandToRaspberryPi, notifyClients } = require('./websocket');

// Render halaman login
exports.showLogin = (req, res) => {
    res.render('login');
};

// Tangani login menggunakan Passport.js
exports.handleLogin = (req, res, next) => {
    passport.authenticate('local', (err, user, info) => {
        if (err) {
            console.error('Error during authentication:', err);
            req.session.error = 'Authentication failed';
            //return res.redirect('/admin/login');
        }
        if (!user) {
            req.session.error = info.message;
            return res.redirect('/admin/login');
        }
        req.logIn(user, (err) => {
            if (err) {
                console.error('Error during login:', err);
                req.session.error = 'Login failed';
                return res.redirect('/admin/login');
            }
            req.session.isAdmin = true; // Set session variable to indicate admin login
            return res.redirect('/admin/dashboard');
        });
    })(req, res, next);
};

// Tambahkan fungsi untuk mendaftarkan user baru (opsional)
exports.registerUser = async (req, res) => {
    const { username, password } = req.body;

    try {
        // Hash password sebelum menyimpannya ke database
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        // Simpan user ke database
        await db.query('INSERT INTO users (username, password) VALUES ($1, $2)', [username, hashedPassword]);
        res.send('User registered successfully');
    } catch (error) {
        console.error('Error registering user:', error);
        res.status(500).send('Error registering user');
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