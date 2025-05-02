const express = require('express');
const router = express.Router();
const sensorController = require('../controllers/sensorController');

router.post('/sensor-data', sensorController.receiveSensorData);

module.exports = router;