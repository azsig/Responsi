const db = require('../config/db');

// Menampilkan dashboard
exports.showDashboard = async (req, res) => {
  try {
    const result = await db.query('SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1');
    const data = result.rows[0];
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
    const result = await db.query('SELECT * FROM sensor_data ORDER BY id ASC OFFSET $1 LIMIT 1', [index]);
    const data = result.rows[0];
    if (data) {
      res.json(data); // Kirim data dalam format JSON
    } else {
      res.status(404).send('No data found for the given index');
    }
  } catch (error) {
    console.error(error);
    res.status(500).send('Error fetching data by index');
  }
};