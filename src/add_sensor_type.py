from database import sensor_types_collection


sensor_name = input("Unesi naziv novog tipa senzora: ")

metrics = {}

print("\nUnosi metrike senzora.")
print("Kad završiš, upiši 'kraj'.")

while True:
    metric_name = input("\nNaziv metrike: ")

    if metric_name.lower() == "kraj":
        break

    minimum = float(input("Minimalna vrijednost: "))
    maximum = float(input("Maksimalna vrijednost: "))

    metrics[metric_name] = {
        "min": minimum,
        "max": maximum
    }


location_input = input("\nKoristi li senzor lokaciju? (da/ne): ")

has_location = location_input.lower() == "da"


new_sensor_type = {
    "name": sensor_name,
    "metrics": metrics,
    "has_location": has_location
}


sensor_types_collection.insert_one(new_sensor_type)

print(f"\nNovi tip senzora uspješno dodan: {sensor_name}")