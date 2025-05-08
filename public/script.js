console.log('Data received in script.js:', userData);

// Function to update the thermometer
function updateThermometer(selector, temperature, max = 100) {
    const mercury = document.querySelector(selector + " " + '.thermometer .mercury');
    if (mercury) {
        const height = Math.min((temperature / max) * 100, 100); // Calculate height percentage
        mercury.style.height = `${height}%`;
        mercury.style.backgroundColor = height > 50 ? 'red' : 'green';
    }
}

// Function to fetch the latest data from the server
async function fetchLatestData() {
    try {
        const response = await fetch('/dashboard/data/0'); // Endpoint untuk mendapatkan data terbaru
        if (response.ok) {
            const data = await response.json();

            // Update DOM elements dynamically based on their existence
            const temperatureBox = document.querySelector('#temperature .box');
            if (temperatureBox) temperatureBox.textContent = `${data.temperature}°C`;

            const humidityBox = document.querySelector('#humidity .box');
            if (humidityBox) humidityBox.textContent = `${data.humidity}%`;

            const co2Box = document.querySelector('#co2 .box');
            if (co2Box) co2Box.textContent = `${data.co2} ppm`;

            const lpgBox = document.querySelector('#lpg .box');
            if (lpgBox) lpgBox.textContent = `${data.lpg} ppm`;

            const noiseBox = document.querySelector('#noise .box');
            if (noiseBox) noiseBox.textContent = `${data.noise} dB`;

            // Update thermometer and speedometers
            updateThermometer('#temperature', data.temperature, 100); // Max 100°C
            updateThermometer('#humidity', data.humidity, 100); // Max 100%
            updateThermometer('#co2', data.co2, 1000); // Max 1000 ppm
            updateThermometer('#lpg', data.lpg, 1000); // Max 1000 ppm
            updateThermometer('#noise', data.noise, 120); // Max 120 dB

            console.log('Latest data fetched:', data);
        } else {
            console.log('Failed to fetch the latest data');
        }
    } catch (error) {
        console.error('Error fetching the latest data:', error);
    }
}

let pollingIntervalId;

// Function to start polling data every 1 minute
function startPolling() {
    fetchLatestData(); // Fetch data immediately on page load
    pollingIntervalId = setInterval(fetchLatestData, 10000); // Fetch data every 60 seconds
}

// WebSocket for real-time updates
function setupWebSocket() {
    const ws = new WebSocket('ws://localhost:3000?type=web'); // Ganti dengan URL WebSocket server Anda

    ws.onmessage = (event) => {
        console.log('WebSocket message received:', event.data);

        if(event.data === "update"){
            try {
                if(pollingIntervalId){
                    clearInterval(pollingIntervalId); // Clear the previous interval    
                    console.log("Polling interval cleared");
                }
                fetchLatestData(); // Fetch the latest data immediately
    
                console.log('Dashboard updated with WebSocket data:');
            } catch (error) {
                console.error('Error processing WebSocket message:', error);
            }
        }
        
    };

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