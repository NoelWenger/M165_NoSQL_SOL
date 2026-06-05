from pymongo import MongoClient

uri = "mongodb+srv://Wengsi:1234@cluster0.ghns1ap.mongodb.net/?appName=Cluster0"

try:
    client = MongoClient(uri)
    
    server_info = client.server_info()
    
    print("--- Verbindung erfolgreich! ---")
    print(f"MongoDB Version: {server_info['version']}")
    
    print("\nVerfügbare Datenbanken:")
    for db_name in client.list_database_names():
        print(f" - {db_name}")

except Exception as e:
    print("--- Verbindung fehlgeschlagen! ---")
    print(f"Fehlerursache: {e}")