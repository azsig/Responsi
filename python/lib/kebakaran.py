import smbus2
import time
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setwarnings(False)  # Menonaktifkan peringatan jika pin sudah digunakan
GPIO.setmode(GPIO.BCM)

# Tentukan pin yang digunakan
SERVO_PIN_1 = 13  # Servo pertama
SERVO_PIN_2 = 12  # Servo kedua
BUZZER_PIN = 16   # Buzzer (active low)

# Setup GPIO pin untuk servo dan buzzer
GPIO.setup(SERVO_PIN_1, GPIO.OUT)
GPIO.setup(SERVO_PIN_2, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Setup PWM untuk kontrol servo
servo_pwm_1 = GPIO.PWM(SERVO_PIN_1, 50)  # 50Hz PWM frequency
servo_pwm_2 = GPIO.PWM(SERVO_PIN_2, 50)  # 50Hz PWM frequency
servo_pwm_1.start(0)  # Mulai dengan servo di posisi 0 derajat
servo_pwm_2.start(0)  # Mulai dengan servo di posisi 0 derajat

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

# Fungsi untuk menggerakkan servo ke 180 derajat
def move_servos_to_180():
    servo_pwm_1.ChangeDutyCycle(10)  # 180 derajat untuk servo pertama
    servo_pwm_2.ChangeDutyCycle(10)  # 180 derajat untuk servo kedua

# Fungsi untuk menggerakkan servo ke 0 derajat
def move_servos_to_0():
    servo_pwm_1.ChangeDutyCycle(2)  # 0 derajat untuk servo pertama
    servo_pwm_2.ChangeDutyCycle(2)  # 0 derajat untuk servo kedua

# Fungsi untuk menyalakan buzzer (active low)
def activate_buzzer():
    GPIO.output(BUZZER_PIN, GPIO.LOW)  # Nyalakan buzzer (active low)

# Fungsi untuk mematikan buzzer (active low)
def deactivate_buzzer():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Matikan buzzer (active low)

# Loop terus menerus untuk membaca suhu dan mengontrol perangkat
try:
    while True:
        temp, humidity = read_sht20()
        if temp is not None and humidity is not None:
            print(f"Temperature (°C): {temp:.2f}")
            print(f"Humidity (%RH): {humidity:.2f}")
            print("-" * 30)

            # Cek suhu dan kontrol servo + buzzer
            if temp >= 35.0:
                move_servos_to_180()  # Gerakkan servo ke 180 derajat
                deactivate_buzzer()     # Nyalakan buzzer
            else:
                move_servos_to_0()    # Kembalikan servo ke 0 derajat
                activate_buzzer()   # Matikan buzzer

        time.sleep(2)  # delay 2 detik sebelum baca lagi

except KeyboardInterrupt:
    print("Stopped by user.")
    GPIO.cleanup()  # Bersihkan pengaturan GPIO saat program dihentikan
