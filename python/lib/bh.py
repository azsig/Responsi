import smbus
import time
import aktuator


# Alamat I2C BH1750
DEVICE1 = 0x23
DEVICE2 = 0x5C
CONTINUOUS_HIGH_RES_MODE = 0x10

# Setup I2C
bus = smbus.SMBus(1)

# Setup GPIO


# Fungsi untuk membaca lux
def read_light(addr=DEVICE1):
    data = bus.read_i2c_block_data(addr, CONTINUOUS_HIGH_RES_MODE, 2)
    result = (data[0] << 8) + data[1]
    lux = result / 1.2
    return lux

def read_inLight(addr=DEVICE2):
    data = bus.read_i2c_block_data(addr, CONTINUOUS_HIGH_RES_MODE, 2)
    result = (data[0] << 8) + data[1]
    lux = result / 1.2
    return lux

def lightLogic():
    try:
        while True:
            light_level = read_light()
            print(f"Cahaya: {light_level:.2f} lux")

            if light_level < 300:
                print("Lux < 300 → Relay ON") # Relay ON
                aktuator.relay_on()
            else:
                print("Lux ≥ 300 → Relay OFF")
                aktuator.relay_off()  # Relay OFF

            time.sleep(1)

    except KeyboardInterrupt:
        print("Program dihentikan")



