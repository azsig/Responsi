import aktuator
import time
import RPi.GPIO as GPIO
from pintu5 import check_pir


def lightLogic(light):
    try:
        while True:
            light_level = light
            print(f"Cahaya: {light_level:.2f} lux")

            if light_level < 300:
                print("Lux < 300 → Relay ON") # Relay ON
                aktuator.buzzer_on()
            else:
                print("Lux ≥ 300 → Relay OFF")
                aktuator.buzzer_off()  # Relay OFF

            time.sleep(1)

    except KeyboardInterrupt:
        print("Program dihentikan")

def kebakaranLogic(temp, humidity):
    try:
        while True:
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

last_servo_position = None
def co2Logic(co2):
    try:
        while True:
            co2_concentration = co2
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            if co2_concentration is not None:
                print(f"{timestamp} - CO2: {co2_concentration} ppm")

                # Menghindari perubahan berulang jika posisi servo sudah sesuai dengan kondisi CO2
                if co2_concentration > 990 and last_servo_position != 180:
                    print("Kadar CO2 lebih dari 1000 ppm, menggerakkan servo ke 180 derajat.")
                    aktuator.move_pintu(180)  # Menggerakkan servo ke posisi 180 derajat
                    last_servo_position = 180  # Simpan posisi servo saat ini
                elif co2_concentration <= 990 and last_servo_position != 0:
                    print("Kadar CO2 normal, menggerakkan servo ke 0 derajat.")
                    aktuator.move_pintu(0)  # Menggerakkan servo kembali ke posisi awal (0 derajat)
                    last_servo_position = 0  # Simpan posisi servo saat ini
            else:
                print("Gagal membaca data dari sensor.")

            time.sleep(0.5)  # Delay 0.5 detik sebelum membaca ulang

    except KeyboardInterrupt:
        print("\nPengukuran dihentikan.")

lastState = None
def modbusLogic(analog):
    try:
        while True:
            try:
                analog1 = analog  # A1 di register ke-3
                print(f"A1: {analog1}", end="\r")

                if analog1 > 200:
                    if lastState != "open":
                        aktuator.move_jendela(180)  # Gerakkan servo ke 180 derajat
                        window_open = True

                else:
                    if lastState != "close":
                        aktuator.move_jendela(0)  # Gerakkan servo ke 0 derajat
                        window_open = False

            except Exception as e:
                print("❌ Error:", e)

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n⛔ Dihentikan oleh pengguna.")

def pintuLogic():
    try:
        # Pastikan pintu tertutup saat program pertama kali dijalankan
        print("Sistem Pintu Otomatis Dimulai...")
        aktuator.move_pintu(0)  # Pintu tertutup pada awal program
        check_pir()

    except KeyboardInterrupt:
        print("Program dihentikan oleh pengguna.")

    finally:
        GPIO.cleanup()  # Membersihkan GPIO untuk menghindari konflik pin
