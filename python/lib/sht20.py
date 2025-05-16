import smbus2
import time
import aktuator
# Setup GPIO


# Setup GPIO pin untuk servo dan buzzer


# Setup PWM untuk kontrol servo

# Fungsi untuk membaca sensor SHT20
def read_sht20():
    try:
        bus = smbus2.SMBus(1)  # Gunakan I2C bus 1
        address = 0x40  # Alamat I2C untuk SHT20 sensor

        # Baca suhu
        write = smbus2.i2c_msg.write(address, [0xF3])  # Perintah untuk baca suhu
        bus.i2c_rdwr(write)
        time.sleep(0.5)  # Tunggu konversi selesai
        read = smbus2.i2c_msg.read(address, 2)  # Baca 2 byte data suhu
        bus.i2c_rdwr(read)
        data = list(read)
        temp_raw = (data[0] << 8) + data[1]
        temp = temp_raw * 175.72 / 65536 - 46.85

        # Baca kelembapan
        write = smbus2.i2c_msg.write(address, [0xF5])  # Perintah untuk baca kelembapan
        bus.i2c_rdwr(write)
        time.sleep(0.5)  # Tunggu konversi selesai
        read = smbus2.i2c_msg.read(address, 2)  # Baca 2 byte data kelembapan
        bus.i2c_rdwr(read)
        data = list(read)
        humid_raw = (data[0] << 8) + data[1]
        humidity = humid_raw * 125 / 65536 - 6

        return temp, humidity
    except OSError as e:
        print(f"Error: {e}")
        return None, None

def kebakaranLogic():
    try:

        while True:
            temp, humidity = read_sht20()
            if temp is not None and humidity is not None:
                print(f"Temperature (°C): {temp:.2f}")
                print(f"Humidity (%RH): {humidity:.2f}")
                print("-" * 30)

                # Cek suhu dan kontrol servo + buzzer
                if temp >= 35.0:
                    aktuator.move_pintu(180)  # Gerakkan servo ke 180 derajat
                    aktuator.move_jendela(180)  # Gerakkan servo ke 180 derajat
                    aktuator.buzzer_on()
                    print("🔥 Suhu tinggi! Pintu dan jendela terbuka, buzzer menyala.")
                else:
                    aktuator.move_pintu(0)
                    aktuator.move_jendela(0)
                    aktuator.buzzer_off()
                    print("Suhu normal. Pintu dan jendela tertutup, buzzer mati.")

            time.sleep(2)  # delay 2 detik sebelum baca lagi

    except KeyboardInterrupt:
        print("Stopped by user.")
        GPIO.cleanup()  # Bersihkan pengaturan GPIO saat program dihentikan
