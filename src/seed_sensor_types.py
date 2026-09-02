from database import sensor_types_collection


sensor_types_collection.delete_many({})


sensor_types = [
    {
        "name": "running",
        "metrics": {
            "heart_rate": {"min": 100, "max": 200},
            "speed": {"min": 2, "max": 10},
            "distance": {"min": 100, "max": 15000}
        },
        "has_location": True
    },
    {
        "name": "cycling",
        "metrics": {
            "heart_rate": {"min": 90, "max": 190},
            "speed": {"min": 10, "max": 60},
            "power": {"min": 100, "max": 500},
            "cadence": {"min": 50, "max": 120}
        },
        "has_location": False
    },
    {
        "name": "performance",
        "metrics": {
            "acceleration": {"min": 0.5, "max": 5},
            "jump_height": {"min": 20, "max": 100},
            "force": {"min": 500, "max": 2500}
        },
        "has_location": False
    }
]


sensor_types_collection.insert_many(sensor_types)

print("Uspješno dodane definicije senzora.")