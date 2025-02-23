# test_mongo_connection.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    print("Connexion à MongoDB réussie")
except Exception as e:
    print(f"Échec de la connexion à MongoDB: {e}")
