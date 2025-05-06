const express = require('express');
const router = express.Router();
const adminController = require('../controllers/adminController');
const { ensureAuthenticated } = require('../middleware/auth');

// Rute login
router.get('/login', adminController.showLogin);
router.post('/login', adminController.handleLogin);

// Rute dashboard (hanya untuk user yang sudah login)
router.get('/dashboard', ensureAuthenticated, adminController.showAdminDashboard);

// Rute untuk mendaftarkan user baru (opsional)
router.post('/register', adminController.registerUser);

router.post('/emergency', adminController.handleEmergency);

module.exports = router;