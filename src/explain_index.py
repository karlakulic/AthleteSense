from database import sensor_readings_collection


ATHLETE_ID = 50

def explain_query():

    command = {
        "explain": {
            "find": "sensor_readings",
            "filter": {"athlete_id": ATHLETE_ID}
        },
        "verbosity": "executionStats"
    }

    return sensor_readings_collection.database.command(command)


print("=== BEZ INDEKSA ===")

sensor_readings_collection.drop_indexes()

explain_without_index = explain_query()

stats_without = explain_without_index["executionStats"]

print("Broj pronađenih dokumenata:", stats_without["nReturned"])
print("Broj pregledanih dokumenata:", stats_without["totalDocsExamined"])
print("Broj pregledanih zapisa indeksa:", stats_without["totalKeysExamined"])
print("Vrijeme izvršavanja:", stats_without["executionTimeMillis"], "ms")


sensor_readings_collection.create_index("athlete_id")

print("\n=== S INDEKSOM ===")

explain_with_index = explain_query()

stats_with = explain_with_index["executionStats"]

print("Broj pronađenih dokumenata:", stats_with["nReturned"])
print("Broj pregledanih dokumenata:", stats_with["totalDocsExamined"])
print("Broj pregledanih zapisa indeksa:", stats_with["totalKeysExamined"])
print("Vrijeme izvršavanja:", stats_with["executionTimeMillis"], "ms")

print("\n=== USPOREDBA ===")

print(
    "Bez indeksa MongoDB je pregledao:",
    stats_without["totalDocsExamined"],
    "dokumenata"
)

print(
    "S indeksom MongoDB je pregledao:",
    stats_with["totalDocsExamined"],
    "dokumenata"
)

saved = (
    stats_without["totalDocsExamined"]
    - stats_with["totalDocsExamined"]
)

print("Indeks je izbjegao pregled:", saved, "dokumenata")