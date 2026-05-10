import os
import time
import random
import requests
from datetime import datetime

API_URL = os.getenv("API_URL", "http://localhost:8000")
DRONES = int(os.getenv("DRONES", "3"))
INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS", "5"))

DRONE_IDS = [f"drone-{i:03d}" for i in range(1, DRONES + 1)]

FIELD_ZONES = [
    {"lat": 6.2442, "lon": -75.5812},
    {"lat": 6.2530, "lon": -75.5900},
    {"lat": 6.2380, "lon": -75.5750},
]


def generate_reading(drone_id: str) -> dict:
    zone = random.choice(FIELD_ZONES)
    return {
        "drone_id": drone_id,
        "latitude":  zone["lat"] + random.uniform(-0.001, 0.001),
        "longitude": zone["lon"] + random.uniform(-0.001, 0.001),
        "temperature_celsius": round(random.uniform(18.0, 35.0), 2),
        "humidity_percent":    round(random.uniform(40.0, 90.0), 2),
        "ndvi":                round(random.uniform(0.1, 0.9), 4),
        "altitude_meters":     round(random.uniform(30.0, 120.0), 1),
    }


def send_reading(drone_id: str):
    reading = generate_reading(drone_id)
    try:
        response = requests.post(
            f"{API_URL}/ingest",
            json=reading,
            timeout=5
        )
        if response.status_code == 200:
            print(f"[{drone_id}] Reading sent OK — NDVI: {reading['ndvi']} Temp: {reading['temperature_celsius']}°C")
        else:
            print(f"[{drone_id}] Error {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        print(f"[{drone_id}] Could not connect to API at {API_URL}")


def main():
    print(f"[simulator] Starting with {DRONES} drones, interval {INTERVAL_SECONDS}s")
    print(f"[simulator] Target API: {API_URL}")
    print(f"[simulator] Drones: {DRONE_IDS}")

    time.sleep(3)

    while True:
        for drone_id in DRONE_IDS:
            send_reading(drone_id)
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
