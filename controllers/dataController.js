const db = require('../config/db');

exports.showAddDataForm = (req, res) => {
  res.render('addData');
};

exports.addData = async (req, res) => {
  const { temperature, humidity, co2, lpg, noise } = req.body;

  try {
    await db.query(
      'INSERT INTO sensor_data (temperature, humidity, co2, lpg, noise) VALUES ($1, $2, $3, $4, $5)',
      [temperature, humidity, co2, lpg, noise]
    );
    res.redirect('/dashboard');
  } catch (error) {
    console.error(error);
    res.status(500).send('Error adding data');
  }
};