#!/usr/bin/env python3
import minimalmodbus
import serial
import time
import RPi.GPIO as GPIO

# --- GPIO Setup ---
SERVO_PIN = 13
BUZZER_PIN = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Servo PWM 50Hz
servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(0)

# --- Modbus Setup ---
instrument = minimalmodbus.Instrument('/dev/ttyUSB1', 10)
instrument.serial.baudrate = 19200
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = 1
instrument.mode = minimalmodbus.MODE_RTU

print("🔄 Monitoring nilai A1 untuk kontrol jendela otomatis...\nTekan Ctrl+C untuk keluar.\n")

# Status jendela (False = tertutup, True = terbuka)
window_open = False

def buka_jendela():
    print("🪟 Membuka jendela (servo ke 180°)")
    servo_pwm.ChangeDutyCycle(12.5)  # 180°
    time.sleep(0.5)
    servo_pwm.ChangeDutyCycle(0)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

def tutup_jendela():
    print("🪟 Menutup jendela (servo ke 0°)")
    servo_pwm.ChangeDutyCycle(2.5)  # 0°
    time.sleep(0.5)
    servo_pwm.ChangeDutyCycle(0)
    GPIO.output(BUZZER_PIN, GPIO.LOW)

try:
    while True:
        try:
            analog1 = instrument.read_register(3, 0)  # A1 di register ke-3
            print(f"A1: {analog1}", end="\r")

            if analog1 > 200 and not window_open:
                buka_jendela()
                window_open = True

            elif analog1 <= 200 and window_open:
                tutup_jendela()
                window_open = False

        except minimalmodbus.NoResponseError:
            print("⚠️  Tidak ada respon dari Arduino. Cek koneksi.")

        except Exception as e:
            print("❌ Error:", e)

        time.sleep(1)

except KeyboardInterrupt:
    print("\n⛔ Dihentikan oleh pengguna.")

finally:
    servo_pwm.stop()
    GPIO.cleanup()
