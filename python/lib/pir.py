import RPi.GPIO as GPIO
import time
import aktuator

# Setup GPIO
PIR_IN_PIN = 23
PIR_OUT_PIN = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_IN_PIN, GPIO.IN)
GPIO.setup(PIR_OUT_PIN, GPIO.IN)

# Variabel untuk menghitung jumlah orang di dalam ruangan
jumlah_orang = 0

# Fungsi untuk menggerakkan servo


def wait_for_motion(pin):
    # Tunggu sampai ada deteksi gerakan di pin tertentu
    print(f"Menunggu gerakan di pin {pin}...")
    while GPIO.input(pin) == GPIO.LOW:
        time.sleep(0.1)
    print(f"Gerakan terdeteksi di pin {pin}.")

    # Tunggu sedikit lebih lama agar sinyal stabil
    time.sleep(0.5)  # Menambahkan sedikit waktu delay untuk stabilisasi sinyal

    # Tunggu sampai tidak ada gerakan lagi
    while GPIO.input(pin) == GPIO.HIGH:
        time.sleep(0.1)
    print(f"Tidak ada gerakan lagi di pin {pin}.")

def check_pir():
    global jumlah_orang  # Mengakses variabel jumlah_orang
    while True:
        pir_out_state = GPIO.input(PIR_OUT_PIN)
        pir_in_state = GPIO.input(PIR_IN_PIN)

        if pir_out_state == GPIO.HIGH:
            print("Gerakan di luar terdeteksi - Membuka pintu")
            aktuator.move_pintu(90)  # Servo buka pintu
            time.sleep(1)   # Memberi waktu untuk servo bergerak
            wait_for_motion(PIR_IN_PIN)  # Tunggu gerakan di dalam
            print("Orang masuk - Menutup pintu")
            aktuator.move_pintu(0)  # Servo tutup pintu
            time.sleep(1)  # Memberi waktu untuk servo menutup pintu
            jumlah_orang += 1  # Tambah jumlah orang yang ada di dalam ruangan
            print(f"Jumlah orang dalam ruangan: {jumlah_orang}")

        elif pir_in_state == GPIO.HIGH:
            print("Gerakan di dalam terdeteksi - Membuka pintu")
            aktuator.move_pintu(90)  # Servo buka pintu
            time.sleep(1)   # Memberi waktu untuk servo bergerak
            wait_for_motion(PIR_OUT_PIN)  # Tunggu gerakan di luar
            print("Orang keluar - Menutup pintu")
            aktuator.move_pintu(0)  # Servo tutup pintu
            time.sleep(1)  # Memberi waktu untuk servo menutup pintu
            jumlah_orang -= 1  # Kurangi jumlah orang yang ada di dalam ruangan
            print(f"Jumlah orang dalam ruangan: {jumlah_orang}")

        time.sleep(0.1)  # Memberikan sedikit delay agar tidak terlalu sering memeriksa status PIR

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
