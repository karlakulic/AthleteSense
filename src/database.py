from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["athletesense_db"]

athletes_collection = db["athletes"]
devices_collection = db["devices"]
sensor_readings_collection = db["sensor_readings"]
sensor_types_collection = db["sensor_types"]