#!/usr/bin/env python3
import minimalmodbus
import serial
import time
import aktuator

# --- GPIO Setup ---



# Servo PWM 50Hz

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



def read():
    try:
        analog1 = instrument.read_register(3, 0)
        analog0 = instrument.read_register(2, 0)
        return analog1, analog0
    except minimalmodbus.NoResponseError:
        print("⚠️  Tidak ada respon dari Arduino. Cek koneksi.")
lastState = None
def modbusLogic():
    try:
        while True:
            try:
                analog1 = instrumen.read_register(3,0)  # A1 di register ke-3
                print(f"A1: {analog1}", end="\r")

                if analog1 > 200:
                    if lastState != "open":
                        aktuator.move_jendela(180)  # Gerakkan servo ke 180 derajat
                        window_open = True

                else:
                    if lastState != "close":
                        aktuator.move_jendela(0)  # Gerakkan servo ke 0 derajat
                        window_open = False

            except Exception as e:
                print("❌ Error:", e)

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n⛔ Dihentikan oleh pengguna.")


