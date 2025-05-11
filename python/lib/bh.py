import smbus
import time
import RPi.GPIO as GPIO

# Alamat I2C BH1750
DEVICE = 0x23
CONTINUOUS_HIGH_RES_MODE = 0x10

# Setup I2C
bus = smbus.SMBus(1)

# Setup GPIO
RELAY_PIN = 16  # Ganti dengan pin GPIO yang kamu pakai
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH)  # Relay OFF awalnya (asumsi active low)

# Fungsi untuk membaca lux
def read_light(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, CONTINUOUS_HIGH_RES_MODE, 2)
    result = (data[0] << 8) + data[1]
    lux = result / 1.2
    return lux

try:
    while True:
        light_level = read_light()
        print(f"Cahaya: {light_level:.2f} lux")

        if light_level < 300:
            print("Lux < 300 → Relay ON")
            GPIO.output(RELAY_PIN, GPIO.LOW)  # Relay ON (asumsi active low)
        else:
            print("Lux ≥ 300 → Relay OFF")
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Relay OFF

        time.sleep(1)

except KeyboardInterrupt:
    print("Program dihentikan")

finally:
    GPIO.cleanup()
