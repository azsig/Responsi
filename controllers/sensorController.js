const db = require('../config/db');

exports.receiveSensorData = async (req, res) => {
    const { temperature, humidity, co2, lpg, noise } = req.body;

    try {
        // Simpan data ke database
        await db.query(
            'INSERT INTO sensor_data (temperature, humidity, co2, lpg, noise, updated_at) VALUES ($1, $2, $3, $4, $5, NOW())',
            [temperature, humidity, co2, lpg, noise]
        );
        console.log('Sensor data received and saved:', { temperature, humidity, co2, lpg, noise });
        res.status(200).send('Sensor data received');
    } catch (error) {
        console.error('Error saving sensor data:', error);
        res.status(500).send('Error saving sensor data');
    }
};
