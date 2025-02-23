from .config import MONGO_DB_URI, DATABASE_NAME
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(MONGO_DB_URI)
database = client[DATABASE_NAME]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Collection Definition
SENSOR_COLLECTION = database["sensors"]