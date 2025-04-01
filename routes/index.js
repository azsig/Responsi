const express = require('express');
const router = express.Router();
const dataController = require('../controllers/dataController');

router.get('/', (req, res) => {
  res.render('home');
});

router.get('/add-data', dataController.showAddDataForm);
router.post('/add-data', dataController.addData);

module.exports = router;