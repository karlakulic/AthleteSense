from database import sensor_readings_collection


pipeline_heart_rate = [
    {
        "$match": {
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
        "$limit": 10
    }
]


results = sensor_readings_collection.aggregate(
    pipeline_heart_rate
)


print("=== TOP 10 SPORTAŠA PREMA PROSJEČNOM PULSU ===")

for result in results:
    print(
        f"Sportaš {result['_id']} | "
        f"Prosječni puls: {result['average_heart_rate']:.2f} | "
        f"Max puls: {result['max_heart_rate']} | "
        f"Broj mjerenja: {result['number_of_readings']}"
    )


pipeline_all_metrics = [
    {
        "$project": {
            "sensor_type": 1,
            "metrics": {
                "$objectToArray": "$metrics"
            }
        }
    },
    {
        "$unwind": "$metrics"
    },
    {
        "$group": {
            "_id": {
                "sensor_type": "$sensor_type",
                "metric": "$metrics.k"
            },
            "average": {
                "$avg": "$metrics.v"
            },
            "minimum": {
                "$min": "$metrics.v"
            },
            "maximum": {
                "$max": "$metrics.v"
            },
            "number_of_values": {
                "$sum": 1
            }
        }
    },
    {
        "$sort": {
            "_id.sensor_type": 1,
            "_id.metric": 1
        }
    }
]


results = sensor_readings_collection.aggregate(
    pipeline_all_metrics
)


print("\n=== ANALIZA SVIH VRSTA SENZORA ===")

current_sensor_type = None

for result in results:

    sensor_type = result["_id"]["sensor_type"]
    metric = result["_id"]["metric"]

    if sensor_type != current_sensor_type:
        print(f"\n{sensor_type.upper()}")
        current_sensor_type = sensor_type

    print(
        f"{metric} | "
        f"Prosjek: {result['average']:.2f} | "
        f"Min: {result['minimum']} | "
        f"Max: {result['maximum']} | "
        f"Broj vrijednosti: {result['number_of_values']}"
    )