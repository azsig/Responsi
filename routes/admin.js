const express = require('express');
const router = express.Router();
const adminController = require('../controllers/adminController');

router.get('/login', adminController.showLogin);
router.post('/login', adminController.handleLogin);
router.get('/dashboard', adminController.showAdminDashboard);
router.post('/emergency', adminController.handleEmergency);
router.get('/data/:index', adminController.getDataByIndex);

module.exports = router;