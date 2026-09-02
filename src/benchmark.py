import time

from database import sensor_readings_collection
from generate_data import generate_sensor_reading


TEST_SIZE = 10000
BATCH_SIZE = 1000


def test_insert_one():
    sensor_readings_collection.delete_many({})

    start_time = time.perf_counter()

    for i in range(TEST_SIZE):
        sensor_readings_collection.insert_one(generate_sensor_reading())

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    throughput = TEST_SIZE / elapsed_time

    return elapsed_time, throughput


def test_insert_many():
    sensor_readings_collection.delete_many({})

    start_time = time.perf_counter()

    inserted_count = 0

    while inserted_count < TEST_SIZE:
        batch = []

        remaining = TEST_SIZE - inserted_count
        current_batch_size = min(BATCH_SIZE, remaining)

        for i in range(current_batch_size):
            batch.append(generate_sensor_reading())

        sensor_readings_collection.insert_many(batch)

        inserted_count += current_batch_size

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    throughput = TEST_SIZE / elapsed_time

    return elapsed_time, throughput


print("Testiranje insert_one()...")

one_time, one_throughput = test_insert_one()

print("Testiranje insert_many()...")

many_time, many_throughput = test_insert_many()


print("\n--- BENCHMARK REZULTATI ---")

print(f"insert_one() vrijeme: {one_time:.2f} sekundi")
print(f"insert_one() throughput: {one_throughput:.2f} dokumenata/sekundi")

print()

print(f"insert_many() vrijeme: {many_time:.2f} sekundi")
print(f"insert_many() throughput: {many_throughput:.2f} dokumenata/sekundi")

print()

speedup = many_throughput / one_throughput

print(f"insert_many() je približno {speedup:.2f} puta brži.")