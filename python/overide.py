import aktuator
import time


def runOveride(sudut, sudut2):
    try:
        if sudut2 == 0:
           aktuator.pintu_tutup()
        else:
           aktuator.pintu_buka()
        aktuator.move_jendela(sudut)
        aktuator.buzzer_on()
    except:
        print("error")
    
