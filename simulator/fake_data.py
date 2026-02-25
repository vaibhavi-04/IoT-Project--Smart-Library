import requests
import random
import time

SERVER_URL = "http://127.0.0.1:5000/api/data"

TOTAL_SEATS = 10

def generate_fake_data():
    occupied = random.randint(0, TOTAL_SEATS)
    occupancy_percent = (occupied * 100) / TOTAL_SEATS

    noise_levels = ["Low", "Medium", "High"]
    noise = random.choice(noise_levels)

    return {
        "occupied_seats": occupied,
        "total_seats": TOTAL_SEATS,
        "occupancy_percentage": occupancy_percent,
        "noise_level": noise
    }

while True:
    data = generate_fake_data()
    response = requests.post(SERVER_URL, json=data)
    print("Sent:", data)
    time.sleep(5)