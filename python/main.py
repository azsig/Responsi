from websocket_client import start_websocket_client

if __name__ == "__main__":
    try:
        start_websocket_client()
    except KeyboardInterrupt:
        print("Program stopped by user")