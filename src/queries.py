from database import (
    athletes_collection,
    devices_collection,
    sensor_readings_collection
)


# 1. 
print("\n=== 1. PRVIH 5 RUNNING MJERENJA ===")

running_readings = sensor_readings_collection.find(
    {"sensor_type": "running"}
).limit(5)

for reading in running_readings:
    print(
        f"Sportaš {reading['athlete_id']} | "
        f"Puls: {reading['metrics']['heart_rate']} | "
        f"Brzina: {reading['metrics']['speed']} | "
        f"Udaljenost: {reading['metrics']['distance']}"
    )


# 2. 
print("\n=== 2. RUNNING MJERENJA S PULSOM > 180 ===")

high_heart_rate = sensor_readings_collection.find(
    {
        "sensor_type": "running",
        "metrics.heart_rate": {"$gt": 180}
    }
).limit(5)

for reading in high_heart_rate:
    print(
        f"Sportaš {reading['athlete_id']} | "
        f"Puls: {reading['metrics']['heart_rate']} | "
        f"Brzina: {reading['metrics']['speed']}"
    )


# 3. 
print("\n=== 3. TOP 5 RUNNING MJERENJA PREMA PULSU ===")

top_heart_rate = sensor_readings_collection.find(
    {"sensor_type": "running"}
).sort(
    "metrics.heart_rate", -1
).limit(5)

for reading in top_heart_rate:
    print(
        f"Sportaš {reading['athlete_id']} | "
        f"Puls: {reading['metrics']['heart_rate']} | "
        f"Brzina: {reading['metrics']['speed']}"
    )


# 4. 
print("\n=== 4. SPORTAŠ I NJEGOVI UREĐAJI ===")

athlete = athletes_collection.find_one()

if athlete:
    print(
        f"Sportaš: {athlete['name']} | "
        f"Sport: {athlete['sport']} | "
        f"Godine: {athlete['age']}"
    )

    devices = devices_collection.find(
        {"athlete_id": athlete["_id"]}
    )

    print("Uređaji:")

    for device in devices:
        print(
            f"Uređaj {device['_id']} | "
            f"Tip: {device['type']}"
        )


# 5. 
print("\n=== 5. ANALIZA PULSA PREMA VRSTI SENZORA ===")

pipeline = [
    {
        "$match": {
            "metrics.heart_rate": {"$exists": True}
        }
    },
    {
        "$group": {
            "_id": "$sensor_type",
            "average_heart_rate": {
                "$avg": "$metrics.heart_rate"
            },
            "max_heart_rate": {
                "$max": "$metrics.heart_rate"
            },
            "number_of_readings": {
                "$sum": 1
            }
        }
    },
    {
        "$sort": {
            "average_heart_rate": -1
        }
    }
]

results = sensor_readings_collection.aggregate(pipeline)

for result in results:
    print(
        f"{result['_id'].upper()} | "
        f"Prosječni puls: {result['average_heart_rate']:.2f} | "
        f"Max puls: {result['max_heart_rate']} | "
        f"Broj mjerenja: {result['number_of_readings']}"
    )


# 6. 
print("\n=== 6. TOP 5 SPORTAŠA PREMA PROSJEČNOM RUNNING PULSU ===")

pipeline = [
    {
        "$match": {
            "sensor_type": "running",
            "metrics.heart_rate": {"$exists": True}
        }
    },
    {
        "$group": {
            "_id": "$athlete_id",
            "average_heart_rate": {
                "$avg": "$metrics.heart_rate"
            },
            "max_heart_rate": {
                "$max": "$metrics.heart_rate"
            },
            "number_of_readings": {
                "$sum": 1
            }
        }
    },
    {
        "$sort": {
            "average_heart_rate": -1
        }
    },
    {
        "$limit": 5
    }
]

results = sensor_readings_collection.aggregate(pipeline)

for result in results:
    print(
        f"Sportaš {result['_id']} | "
        f"Prosječni puls: {result['average_heart_rate']:.2f} | "
        f"Max puls: {result['max_heart_rate']} | "
        f"Broj mjerenja: {result['number_of_readings']}"
    )