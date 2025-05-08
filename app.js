const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');
const path = require('path');
const db = require('./config/db');
const { initializeWebSocket, router: websocketRouter } = require('./controllers/websocket');
const http = require('http');
const passport = require('passport');
require('./config/passport')(passport); // Import konfigurasi Passport.js
require('dotenv').config();

const app = express();
const server = http.createServer(app);

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(session({ secret: 'secret', resave: false, saveUninitialized: true }));
app.use(passport.initialize());
app.use(passport.session());
app.use(express.static(path.join(__dirname, 'public')));
app.use((req, res, next) => {
    res.locals.error = req.session.error;
    delete req.session.error; // Hapus pesan setelah ditampilkan
    next();
});

// View Engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Routes
const indexRouter = require('./routes/index');
const dashboardRouter = require('./routes/dashboard');
const adminRouter = require('./routes/admin');
const sensorRoutes = require('./routes/sensor');

app.use('/', indexRouter);
app.use('/dashboard', dashboardRouter);
app.use('/admin', adminRouter);
app.use('/api', sensorRoutes);
app.use('/api/websocket', websocketRouter);

// Initialize WebSocket server
initializeWebSocket(server);

// Start HTTP server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});