import random
import time
from datetime import datetime

from database import (
    sensor_readings_collection,
    devices_collection,
    sensor_types_collection
)


TOTAL_READINGS = 100000
BATCH_SIZE = 1000


devices = list(devices_collection.find())
sensor_types = list(sensor_types_collection.find())


def generate_value(metric_config):
    minimum = metric_config["min"]
    maximum = metric_config["max"]

    if isinstance(minimum, int) and isinstance(maximum, int):
        return random.randint(minimum, maximum)

    return round(random.uniform(minimum, maximum), 2)


def generate_sensor_reading():

    device = random.choice(devices)
    sensor_type = random.choice(sensor_types)

    reading = {
        "athlete_id": device["athlete_id"],
        "device_id": device["_id"],
        "timestamp": datetime.now(),
        "sensor_type": sensor_type["name"],
        "metrics": {}
    }

    for metric_name, metric_config in sensor_type["metrics"].items():
        reading["metrics"][metric_name] = generate_value(metric_config)

    if sensor_type.get("has_location", False):
        reading["location"] = {
            "latitude": round(random.uniform(43.4, 43.6), 6),
            "longitude": round(random.uniform(16.3, 16.6), 6)
        }

    return reading


if __name__ == "__main__":

    print(f"Počinje generiranje {TOTAL_READINGS} dokumenata...")

    start_time = time.perf_counter()

    inserted_count = 0

    while inserted_count < TOTAL_READINGS:

        batch = []

        remaining = TOTAL_READINGS - inserted_count
        current_batch_size = min(BATCH_SIZE, remaining)

        for i in range(current_batch_size):
            batch.append(generate_sensor_reading())

        sensor_readings_collection.insert_many(batch)

        inserted_count += current_batch_size

        print(f"Dodano: {inserted_count}/{TOTAL_READINGS}")

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    throughput = TOTAL_READINGS / elapsed_time

    print("\n--- REZULTATI ---")
    print(f"Ukupno dokumenata: {TOTAL_READINGS}")
    print(f"Vrijeme unosa: {elapsed_time:.2f} sekundi")
    print(f"Throughput: {throughput:.2f} dokumenata/sekundi")