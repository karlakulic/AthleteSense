import time
from datetime import datetime, timedelta

from database import sensor_readings_collection


ATHLETE_ID = 50

end_time = datetime.now()
start_time = end_time - timedelta(minutes=30)


query = {
    "athlete_id": ATHLETE_ID,
    "timestamp": {
        "$gte": start_time,
        "$lte": end_time
    }
}


sensor_readings_collection.drop_indexes()

print("=== BEZ COMPOUND INDEKSA ===")

start = time.perf_counter()

results_without_index = list(
    sensor_readings_collection.find(query)
)

end = time.perf_counter()

time_without_index = end - start

print("Pronađeno dokumenata:", len(results_without_index))
print(f"Vrijeme: {time_without_index:.6f} sekundi")
print("\nStvaram compound index...")

sensor_readings_collection.create_index([
    ("athlete_id", 1),
    ("timestamp", 1)
])


print("\n=== S COMPOUND INDEKSOM ===")

start = time.perf_counter()

results_with_index = list(
    sensor_readings_collection.find(query)
)

end = time.perf_counter()

time_with_index = end - start

print("Pronađeno dokumenata:", len(results_with_index))
print(f"Vrijeme: {time_with_index:.6f} sekundi")

print("\n=== REZULTATI ===")

print(f"Bez compound indeksa: {time_without_index:.6f} sekundi")
print(f"S compound indeksom: {time_with_index:.6f} sekundi")

if time_with_index > 0:
    speedup = time_without_index / time_with_index
    print(f"Upit je približno {speedup:.2f} puta brži.")