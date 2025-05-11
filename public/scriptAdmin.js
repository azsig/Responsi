console.log('Data received in script.js:', userData);

// Function to update the thermometer
function updateThermometer(selector, temperature, max = 100, treshold = 50) {
    const mercury = document.querySelector(selector + " " + '.mercury');
    if (mercury) {
        const height = Math.min((temperature / max) * 100, 100); // Calculate height percentage
        mercury.style.width = `${height}%`;
        mercury.style.backgroundColor = height > treshold ? 'rgba(255, 0, 0, 0.3)' : 'rgba(0, 128, 0, 0.3)';
    }
}

// Function to fetch the latest data from the server
async function fetchLatestData() {
    try {
        const response = await fetch('/dashboard/data/0'); // Endpoint untuk mendapatkan data terbaru
        if (response.ok) {
            const data = await response.json();

            // Update DOM elements dynamically based on the fetched data
            const temperatureBox = document.querySelector('#temperature .text');
            if (temperatureBox) temperatureBox.textContent = `${data.temperature}°C`;

            const humidityBox = document.querySelector('#humidity .text');
            if (humidityBox) humidityBox.textContent = `${data.humidity}%`;

            const co2Box = document.querySelector('#co2 .text');
            if (co2Box) co2Box.textContent = `${data.co2} ppm`;

            const lpgBox = document.querySelector('#lpg .text');
            if (lpgBox) lpgBox.textContent = `${data.lpg} ppm`;

            const noiseBox = document.querySelector('#noise .text');
            if (noiseBox) noiseBox.textContent = `${data.noise} dB`;

            console.log('Latest data fetched:', data);
            // Update thermometer and speedometers
            updateThermometer('#temperature', data.temperature, 100); // Max 100°C
            updateThermometer('#humidity', data.humidity, 100); // Max 100%
            updateThermometer('#co2', data.co2, 1000); // Max 1000 ppm
            updateThermometer('#lpg', data.lpg, 1000); // Max 1000 ppm
            updateThermometer('#noise', data.noise, 120); // Max 120 dB

            // Notify all clients about the new data
            await notifyClients();
        } else {
            console.log('Failed to fetch the latest data');
        }
    } catch (error) {
        console.error('Error fetching the latest data:', error);
    }
}

// Function to notify clients
async function notifyClients() {
    try {
        const response = await fetch('/api/websocket/notify-clients', {
            method: 'POST',
        });
        if (response.ok) {
            console.log('Clients notified successfully');
        } else {
            console.error('Failed to notify clients');
        }
    } catch (error) {
        console.error('Error notifying clients:', error);
    }
}

// Function to start polling data every 1 minute
function startPolling() {
    fetchLatestData(); // Fetch data immediately on page load
    setInterval(fetchLatestData, 10000); // Fetch data every 60 seconds
}

// WebSocket for real-time updates
function setupWebSocket() {
    const ws = new WebSocket('ws://localhost:3000?type=web'); // Ganti dengan URL WebSocket server Anda

    
    ws.onopen = () => {
        console.log('WebSocket connection established');
    };

    ws.onclose = () => {
        console.log('WebSocket connection closed');
    };
}

// Start polling and WebSocket when the page is loaded
document.addEventListener('DOMContentLoaded', () => {
    startPolling();
    setupWebSocket();
});

function formatDate(date) {
    // Format date as e.g. "Monday, 12 June 2024"
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString(undefined, options);   
}
function formatTime(date) {
    // Format time as e.g. "12:34 PM"
    const options = { hour: '2-digit', minute: '2-digit', hour12: true };
    return date.toLocaleTimeString(undefined, options);
}
function updateDateTime() {
    const now = new Date();
    const dateElement = document.getElementById('date');
    const timeElement = document.getElementById('time');
    if (dateElement) {
        dateElement.textContent = formatDate(now);
    }
    if (timeElement) {
        timeElement.textContent = formatTime(now);
    }
}

updateDateTime();
    // Calculate delay then set interval aligned to start of next minute
function startClock() {
    const now = new Date();
    const msToNextMinute = (60 - now.getSeconds()) * 1000 - now.getMilliseconds();
    setTimeout(() => {
        updateDateTime();
        setInterval(updateDateTime, 60000); // update every 60000ms = 1 min
    }, msToNextMinute);
}

startClock();