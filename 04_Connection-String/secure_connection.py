import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

connection_string = os.getenv("MONGO_URI")

def test_secure_connection():
    if not connection_string:
        print("Fehler: MONGO_URI nicht in der .env Datei gefunden!")
        return

    try:
        client = MongoClient(connection_string)
        # Test-Abfrage
        dbs = client.list_database_names()
        print("--- Verbindung erfolgreich über Umgebungsvariable! ---")
        print("Datenbanken:", dbs)
    except Exception as e:
        print(f"Verbindungsfehler: {e}")

if __name__ == "__main__":
    test_secure_connection()

import os
from pymongo import MongoClient