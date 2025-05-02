import random

# Simulate sensor readings
def get_sensor_data():
    return {
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(40, 60), 2),
        "co2": round(random.uniform(300, 500), 2),
        "lpg": round(random.uniform(0, 50), 2),
        "noise": round(random.uniform(30, 70), 2),
    }