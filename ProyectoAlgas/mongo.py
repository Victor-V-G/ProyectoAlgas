from pymongo import MongoClient
from django.conf import settings

def get_mongo_connection():
    uri = getattr(settings, "MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(uri)
    db_name = getattr(settings, "MONGO_DB_NAME", "proyecto_algas_db")
    return client[db_name]
