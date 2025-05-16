import RPi.GPIO as GPIO
import time

PINTU_PIN = 13
JENDELA_PIN = 12
BUZZER_PIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(PINTU_PIN, GPIO.OUT)
GPIO.setup(JENDELA_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)  # Buzzer mati
GPIO.setwarnings(False)  # Menonaktifkan peringatan jika pin sudah digunakan

pintu_pwm = GPIO.PWM(PINTU_PIN, 50)  # 50Hz PWM frequency
jendela_pwm = GPIO.PWM(JENDELA_PIN, 50)  # 50Hz PWM frequency
pintu_pwm.start(0)  # Mulai dengan servo di posisi 0 derajat
jendela_pwm.start(0)  # Mulai dengan servo di posisi 0 derajat
# Fungsi untuk menggerakkan servo pintu
def move_pintu(angle):
    duty = (angle / 18) + 2
    pintu_pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # Memberi waktu untuk servo bergerak
    pintu_pwm.ChangeDutyCycle(0)
# Fungsi untuk menggerakkan servo jendela
def move_jendela(angle):
    duty = (angle / 18) + 2
    jendela_pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # Memberi waktu untuk servo bergerak
    jendela_pwm.ChangeDutyCycle(0)
# Fungsi untuk menyalakan buzzer
def buzzer_on():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Buzzer menyala
# Fungsi untuk mematikan buzzer
def buzzer_off():
    GPIO.output(BUZZER_PIN, GPIO.LOW)  # Buzzer mati