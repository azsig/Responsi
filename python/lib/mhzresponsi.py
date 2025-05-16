import RPi.GPIO as GPIO
import time
import aktuator

# Konfigurasi GPIO untuk pembacaan PWM dari MH-Z19
PWM_PIN = 18  # Sesuaikan dengan pin GPIO yang digunakan untuk pembacaan sensor CO2

# Setup untuk GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.IN)
# Menyimpan status sebelumnya untuk menghindari perubahan berulang


def read_co2_pwm(duration=1.004):
    """Membaca data CO2 dari sensor MH-Z19 melalui sinyal PWM"""
    start_time = time.time()
    high_time = 0
    low_time = 0

    while (time.time() - start_time) < duration:
        if GPIO.input(PWM_PIN) == GPIO.LOW:
            low_start = time.time()
            while GPIO.input(PWM_PIN) == GPIO.LOW:
                pass
            low_time += time.time() - low_start
        if GPIO.input(PWM_PIN) == GPIO.HIGH:
            high_start = time.time()
            while GPIO.input(PWM_PIN) == GPIO.HIGH:
                pass
            high_time += time.time() - high_start

    co2_ppm = 2000 * ((high_time - 0.002) / (high_time + low_time - 0.004))  # Konversi ke ppm (sesuaikan sesuai datasheet)
    return round(co2_ppm)

last_servo_position = None
def co2Logic():
    try:
        while True:
            co2_concentration = read_co2_pwm()  # Membaca konsentrasi CO2
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



