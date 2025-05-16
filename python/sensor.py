from lib import bh
from lib import mhzresponsi
from lib import modbusgacor
from lib import sht20
from lib import pzem004

# Simulate sensor readings
def get_sensor_data():
    temp, humidity = sht20.read_sht20()
    a1, a0 = modbusgacor.read()
    voltage, current, power = pzem004.read_pzem_data()
    return {
        "temperature": temp,
        "humidity": humidity,
        "co2": mhzresponsi.read_co2_pwm(),
        "lpg": a1,
        "noise": a0,
        "light": bh.read_light(),
        "voltage": voltage,
        "current": current,
        "power": power
    }