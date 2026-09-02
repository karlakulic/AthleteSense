import time

from database import sensor_readings_collection
from generate_data import generate_sensor_reading


TEST_SIZES = [10000, 50000, 100000, 250000]
BATCH_SIZE = 1000


def run_test(test_size):
    sensor_readings_collection.delete_many({})

    print(f"\nTestiram {test_size} dokumenata...")

    start_time = time.perf_counter()

    inserted_count = 0

    while inserted_count < test_size:
        batch = []

        remaining = test_size - inserted_count
        current_batch_size = min(BATCH_SIZE, remaining)

        for i in range(current_batch_size):
            batch.append(generate_sensor_reading())

        sensor_readings_collection.insert_many(batch)

        inserted_count += current_batch_size

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time
    throughput = test_size / elapsed_time

    return elapsed_time, throughput


results = []


for size in TEST_SIZES:
    elapsed_time, throughput = run_test(size)

    results.append({
        "documents": size,
        "time": elapsed_time,
        "throughput": throughput
    })


print("\n==============================")
print("      SCALING BENCHMARK")
print("==============================")

for result in results:
    print(
        f"{result['documents']} dokumenata | "
        f"{result['time']:.2f} s | "
        f"{result['throughput']:.2f} dokumenata/s"
    )