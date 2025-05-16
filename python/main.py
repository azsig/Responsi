from websocket_client import start_websocket_client
from runAktuator import runAll
import threading
if __name__ == "__main__":
    try:
        start_websocket_client()
        t1 = threading.Thread(target=runAll)
        t1.start()
    except KeyboardInterrupt:
        print("Program stopped by user")