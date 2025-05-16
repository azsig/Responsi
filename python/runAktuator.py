import threading
from lib import bh
from lib import mhzresponsi
from lib import modbusgacor
from lib import sht20
from lib import logic

def runAll():
    # Simulate sensor readings
    temp, humidity = sht20.read_sht20()
    a1, a0 = modbusgacor.read()
    logic.kebakaranLogic(temp, humidity)
    logic.modbusLogic(a1)
    logic.lightLogic(bh.read_light())
    logic.co2Logic(mhzresponsi.read_co2_pwm())
    logic.pintuLogic()
