import websocket
import json
import threading
import time
from sensor import get_sensor_data
from config import SERVER_URL

# Global variables
stop_sending = False
stop_event = threading.Event()
last_sent_data = None

# Handle messages from server
def on_message(ws, message):
    global stop_sending
    try:
        print("Received command from server:", message)
        command = json.loads(message)
        if command.get("command") == "activate_actuator":
            print("Activating actuator...")
            stop_sending = True
            time.sleep(1)
            print("Actuator activated")
            stop_sending = False
    except json.JSONDecodeError:
        print("Error decoding message")
    except Exception as e:
        print(f"Error processing message: {e}")

# Handle WebSocket connection open
def on_open(ws):
    print("Connected to server")

    # Run send_sensor_data in a separate thread
    threading.Thread(target=send_sensor_data, args=(ws,), daemon=True).start()

# Send sensor data to server
def send_sensor_data(ws):
    global last_sent_data
    while not stop_event.is_set():
        try:
            if not stop_sending:
                data = get_sensor_data()
                if data != last_sent_data:
                    ws.send(json.dumps(data))
                    print("Sent sensor data:", data)
                    last_sent_data = data
        except Exception as e:
            print(f"Error sending data: {e}")
        time.sleep(5)

# Handle WebSocket connection close
def on_close(ws, close_status_code, close_msg):
    print("Disconnected from server. Attempting to reconnect...")
    time.sleep(5)
    reconnect()

# Reconnect to WebSocket server
def reconnect():
    global ws
    ws = websocket.WebSocketApp(
        SERVER_URL,
        on_message=on_message,
        on_open=on_open,
        on_close=on_close,
    )
    ws.run_forever()

# Start WebSocket client
def start_websocket_client():
    global ws
    ws = websocket.WebSocketApp(
        SERVER_URL,
        on_message=on_message,
        on_open=on_open,
        on_close=on_close,
    )
    ws.run_forever()