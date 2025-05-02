const db = require('../config/db');

// Menampilkan dashboard
exports.showDashboard = async (req, res) => {
  try {
    const result = await db.query('SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1');
    const data = result.rows[0];
    console.log('Latest data:', data); // Log the latest data for debugging
    res.render('dashboard', { data });
  } catch (error) {
    console.error(error);
    res.status(500).send('Error fetching data');
  }
};

// Mengambil data berdasarkan indeks
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