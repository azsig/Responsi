const express = require('express');
const bodyParser = require('body-parser');
const session = require('express-session');
const path = require('path');
const db = require('./config/db');
const { initializeWebSocket, router: websocketRouter } = require('./controllers/websocket');
const http = require('http');

const app = express();
const server = http.createServer(app);

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(session({ secret: 'secret', resave: false, saveUninitialized: true }));
app.use(express.static(path.join(__dirname, 'public')));

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
const PORT = 3000;
server.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});