#!/usr/bin/env python3
import minimalmodbus
import serial
import time
import aktuator

# --- GPIO Setup ---



# Servo PWM 50Hz

# --- Modbus Setup ---
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 10)
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

def modbusLogic():
    lastState = "close"
    try:
        while True:
            try:
                analog1 = instrument.read_register(3,0)  # A1 di register ke-3
                print(f"A1: {analog1}", end="\r")

                if analog1 > 100:
                    if lastState != "open":
                        print('test')
                        aktuator.pintu_buka()
                        aktuator.move_jendela(15)  # Gerakkan servo ke 180 derajat
                        window_open = True
                        lastState = "open"

                else:
                    if lastState != "close":
                        print('test2')
                        aktuator.pintu_tutup()
                        aktuator.move_jendela(85)  # Gerakkan servo ke 0 derajat
                        window_open = False
                        lastState = "close"

            except Exception as e:
                print("❌ Error:", e)

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n⛔ Dihentikan oleh pengguna.")


