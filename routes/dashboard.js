const express = require('express');
const router = express.Router();
const dashboardController = require('../controllers/dashboardController');

// Route untuk menampilkan dashboard
router.get('/', dashboardController.showDashboard);

// Route untuk mendapatkan data berdasarkan indeks
router.get('/data/:index', dashboardController.getDataByIndex);

module.exports = router;