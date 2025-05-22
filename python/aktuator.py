import RPi.GPIO as GPIO
import time
from lib import mhzresponsi

PINTU_PIN = 12
JENDELA_PIN = 13
BUZZER_PIN = 16
RELAY_PIN = 17

def define():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PINTU_PIN, GPIO.OUT)
    GPIO.setup(JENDELA_PIN, GPIO.OUT)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    GPIO.output(BUZZER_PIN, GPIO.LOW)  # Buzzer mati
    GPIO.setwarnings(False)  # Menonaktifkan peringatan jika pin sudah digunakan

def define2():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PINTU_PIN, GPIO.OUT)
    GPIO.setup(JENDELA_PIN, GPIO.OUT)
    GPIO.setwarnings(False)  # Menonaktifkan peringatan jika pin sudah digunakan
 
define()

pintu_pwm = GPIO.PWM(PINTU_PIN, 50)  # 50Hz PWM frequency
jendela_pwm = GPIO.PWM(JENDELA_PIN, 50)  # 50Hz PWM frequency
pintu_pwm.start(0)  # Mulai dengan servo di posisi 0 derajat
jendela_pwm.start(0)  # Mulai dengan servo di posisi 0 derajat
# Fungsi untuk menggerakkan servo pintu
def pintu_buka():
    define2()
    duty = 5 
    pintu_pwm.ChangeDutyCycle(duty)
    time.sleep(1.4)  # Memberi waktu untuk servo bergerak
    pintu_pwm.ChangeDutyCycle(0)
def pintu_tutup():
    define2()
    duty = 10
    pintu_pwm.ChangeDutyCycle(duty)
    time.sleep(1.3)
    pintu_pwm.ChangeDutyCycle(0)
# Fungsi untuk menggerakkan servo jendela
def move_jendela(angle):
    define2()
    duty = (angle / 18) + 2
    jendela_pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # Memberi waktu untuk servo bergerak
    jendela_pwm.ChangeDutyCycle(0)
# Fungsi untuk menyalakan relay
def relay_on():
    define() 
def relay_off():
    GPIO.cleanup()
    mhzresponsi.read_co2_pwm()
    GPIO.setmode(GPIO.BCM)  # relay mati
def buzzer_on():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
def buzzer_off():
    GPIO.output(BUZZER_PIN, GPIO.LOW)
