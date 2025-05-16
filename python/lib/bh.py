import smbus
import time
import aktuator


# Alamat I2C BH1750
DEVICE = 0x23
CONTINUOUS_HIGH_RES_MODE = 0x10

# Setup I2C
bus = smbus.SMBus(1)

# Setup GPIO


# Fungsi untuk membaca lux
def read_light(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, CONTINUOUS_HIGH_RES_MODE, 2)
    result = (data[0] << 8) + data[1]
    lux = result / 1.2
    return lux

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



