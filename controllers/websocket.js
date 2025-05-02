const WebSocket = require('ws');
const db = require('../config/db');
const express = require('express');
const router = express.Router();

let wss; // WebSocket server instance

// Initialize WebSocket server
function initializeWebSocket(server) {
    wss = new WebSocket.Server({ server });

    wss.on('connection', (ws) => {
        console.log('Client connected via WebSocket');

        ws.on('message', (message) => {
            console.log('Received data from client:', message); // Log data yang diterima
            try {
                const data = JSON.parse(message); // Parse data yang diterima
                console.log('Parsed data:', data);

                // Simpan data ke database
                db.query(
                    'INSERT INTO sensor_data (temperature, humidity, co2, lpg, noise) VALUES ($1, $2, $3, $4, $5)',
                    [data.temperature, data.humidity, data.co2, data.lpg, data.noise],
                    (err) => {
                        if (err) {
                            console.error('Error saving data to database:', err);
                        } else {
                            console.log('Data saved to database successfully:', data);
                        }
                    }
                );
            } catch (error) {
                console.error('Error processing message:', error);
            }
        });

        ws.on('close', () => {
            console.log('Client disconnected');
        });
    });
}

// Notify all connected clients with the latest data
async function notifyClients() {
    if (!wss) {
        console.error('WebSocket server is not initialized');
        return;
    }

    try {
        // Fetch the latest data from the database
        const result = await db.query('SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1');
        const latestData = result.rows[0];

        if (!latestData) {
            console.error('No data found in the database');
            return;
        }

        console.log('Sending latest data to clients:', latestData); // Debugging log

        // Send the latest data to all connected clients
        wss.clients.forEach((client) => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify(latestData)); // Send the latest data to clients
            }
        });
    } catch (error) {
        console.error('Error fetching or sending data:', error);
    }
}

// Endpoint untuk memicu notifyClients
router.post('/notify-clients', async (req, res) => {
    try {
        await notifyClients();
        res.status(200).send('Clients notified successfully');
    } catch (error) {
        console.error('Error notifying clients:', error);
        res.status(500).send('Error notifying clients');
    }
});

module.exports = {
    initializeWebSocket,
    notifyClients,
    router, // Tambahkan router untuk digunakan di app.js
};