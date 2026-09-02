from database import athletes_collection, devices_collection


athletes_collection.delete_many({})
devices_collection.delete_many({})


athletes = []

sports = [
    "running",
    "cycling",
    "football",
    "basketball",
    "swimming"
]

for i in range(1, 101):
    athlete = {
        "_id": i,
        "name": f"Athlete {i}",
        "sport": sports[(i - 1) % len(sports)],
        "age": 18 + (i % 18)
    }

    athletes.append(athlete)


athletes_collection.insert_many(athletes)


devices = []

for i in range(1, 201):
    device = {
        "_id": i,
        "athlete_id": ((i - 1) % 100) + 1,
        "name": f"Device {i}"
    }

    devices.append(device)


devices_collection.insert_many(devices)


print("Uspješno dodano 100 sportaša.")
print("Uspješno dodano 200 uređaja.")