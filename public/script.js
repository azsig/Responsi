console.log('Data received in script.js:', userData);

// Function to update the thermometer
function updateThermometer(selector, temperature, max = 100) {
    const mercury = document.querySelector(selector+" "+'.thermometer .mercury');
    const maxTemperature = max; // Maximum temperature for the thermometer
    const height = Math.min((temperature / maxTemperature) * 100, 100); // Calculate height percentage
    mercury.style.height = `${height}%`;
    if (height > 50){
      mercury.style.backgroundColor = 'red';
    }
    else{
      mercury.style.backgroundColor = 'green';
    }
  }
  
  // Function to update the speedometer
  // Example: Update the dashboard dynamically
  document.addEventListener('DOMContentLoaded', () => {
    // Replace these values with dynamic data from your server
    const temperature = parseFloat(userData.temperature);
    const humidity = parseFloat(userData.humidity);
    const co2 = parseFloat(userData.co2);
    const lpg = parseFloat(userData.lpg);
    const noise = parseFloat(userData.noise);
  
    // Update thermometer
    updateThermometer('#temperature',temperature, 100); // Max 100°C
  
    // Update speedometers
    updateThermometer('#humidity', humidity, 100); // Max 100%
    updateThermometer('#co2', co2, 1000); // Max 1000 ppm
    updateThermometer('#lpg', lpg, 1000); // Max 1000 ppm
    updateThermometer('#noise', noise, 120); // Max 120 dB

    let currentIndex = 0; // Mulai dari indeks pertama

  // Fungsi untuk mengambil data berdasarkan indeks
  async function fetchDataByIndex(index) {
    try {
      const response = await fetch(`/dashboard/data/${index}`); // Endpoint untuk mendapatkan data berdasarkan indeks
      if (response.ok) {
        const data = await response.json();

        // Update DOM dengan data terbaru
        document.querySelector('#temperature .box').textContent = `${data.temperature}°C`;
        document.querySelector('#humidity .box').textContent = `${data.humidity}%`;
        document.querySelector('#co2 .box').textContent = `${data.co2} ppm`;
        document.querySelector('#lpg .box').textContent = `${data.lpg} ppm`;
        document.querySelector('#noise .box').textContent = `${data.noise} dB`;
        updateThermometer('#temperature',data.temperature, 100); // Max 100°C
  
        // Update speedometers
        updateThermometer('#humidity', data.humidity, 100); // Max 100%
        updateThermometer('#co2', data.co2, 1000); // Max 1000 ppm
        updateThermometer('#lpg', data.lpg, 1000); // Max 1000 ppm
        updateThermometer('#noise', data.noise, 120); // Max 120 dB

        console.log('Data fetched for index', index, ':', data);
        if (index == 5) {
          currentIndex = 0; // Update current index
        }
      } else {
        console.log('No data found for index', index);
      }
    } catch (error) {
      console.error('Error fetching data by index:', error);
    }
  }

  // Fungsi untuk memulai polling data setiap detik
  function startPolling() {
    setInterval(() => {
      fetchDataByIndex(currentIndex); // Ambil data berdasarkan indeks saat ini
      currentIndex++; // Naikkan indeks untuk data berikutnya
    }, 1000); // Interval 1 detik
  }

  // Mulai polling saat halaman dimuat
  startPolling();
  });