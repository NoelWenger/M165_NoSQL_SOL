from pymongo import MongoClient
from bson import ObjectId
import datetime

uri = "mongodb+srv://Wengsi:1234@cluster0.ghns1ap.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client["sample_restaurants"]
col = db["restaurants"]

def list_boroughs():
    print("\n--- 3.1: Stadtbezirke ---")
    results = col.distinct("borough")
    for b in results:
        print(f" - {b}")

def top_3_restaurants():
    print("\n--- 3.2: Top 3 nach Durchschnitts-Rating ---")
    pipeline = [
        {"$unwind": "$grades"},
        {"$group": {
            "_id": "$name", 
            "avgScore": {"$avg": "$grades.score"}
        }},
        {"$sort": {"avgScore": -1}},
        {"$limit": 3}
    ]
    results = col.aggregate(pipeline)
    for res in results:
        print(f" - {res['_id']}: {res['avgScore']:.2f}")

def nearest_to_perigord():
    print("\n--- 3.3: Nächstgelegenes Restaurant zu 'Le Perigord' ---")
    perigord = col.find_one({"name": "Le Perigord"})
    if not perigord:
        print("Restaurant 'Le Perigord' nicht gefunden."); return

    coords = perigord["address"]["coord"]
    query = {
        "address.coord": {
            "$near": {
                "$geometry": {"type": "Point", "coordinates": coords}
            }
        },
        "name": {"$ne": "Le Perigord"}
    }
    nearest = col.find_one(query)
    print(f"Das nächste Restaurant ist: {nearest['name']} in {nearest['borough']}")

def search_and_rate():
    print("\n--- 3.4 & 3.5: Suche & Bewerten ---")
    name_input = input("Suche nach Name (leer lassen für egal): ")
    cuisine_input = input("Suche nach Küche (leer lassen für egal): ")

    query = {}
    if name_input: query["name"] = {"$regex": name_input, "$options": "i"}
    if cuisine_input: query["cuisine"] = {"$regex": cuisine_input, "$options": "i"}

    results = list(col.find(query).limit(10))
    
    if not results:
        print("Keine Restaurants gefunden."); return

    for i, res in enumerate(results):
        print(f"[{i}] {res['name']} ({res['cuisine']})")

    choice = input("\nWähle eine Nummer zum Bewerten (oder Enter zum Abbrechen): ")
    if choice.isdigit() and int(choice) < len(results):
        selected = results[int(choice)]
        score = int(input("Rating (0-100): "))
        
        new_grade = {
            "date": datetime.datetime.now(),
            "grade": "A", # Standardwert
            "score": score
        }
        
        col.update_one({"_id": selected["_id"]}, {"$push": {"grades": new_grade}})
        print(f"Bewertung für {selected['name']} gespeichert!")

def add_restaurant():
    print("\n--- 3.6: Restaurant hinzufügen ---")
    
    def get_input(prompt, min_len):
        while True:
            val = input(prompt)
            if len(val) >= min_len: return val
            print(f"Eingabe zu kurz (min {min_len} Zeichen)!")

    name = get_input("Name: ", 2)
    borough = get_input("Borough: ", 2)
    cuisine = get_input("Cuisine: ", 2)
    building = input("Hausnummer: ")
    street = get_input("Strasse: ", 2)
    
    while True:
        zipcode = input("Postleitzahl (5 Stellen): ")
        if len(zipcode) == 5: break
        print("PLZ muss genau 5 Zeichen lang sein!")

    new_doc = {
        "name": name,
        "borough": borough,
        "cuisine": cuisine,
        "address": {"building": building, "street": street, "zipcode": zipcode, "coord": [0,0]},
        "grades": []
    }
    col.insert_one(new_doc)
    print("Restaurant erfolgreich hinzugefügt!")

# --- 3.7: Restaurant löschen ---
def delete_restaurant():
    print("\n--- 3.7: Restaurant löschen ---")
    search = input("Name des zu löschenden Restaurants: ")
    if len(search) < 2:
        print("Suchbegriff zu kurz!"); return

    query = {"name": {"$regex": search, "$options": "i"}}
    count = col.count_documents(query)
    
    if count == 0:
        print("Keine passenden Restaurants gefunden.")
    else:
        confirm = input(f"Es wurden {count} Restaurants gefunden. Wirklich löschen? (y/n): ")
        if confirm.lower() == 'y':
            col.delete_many(query)
            print(f"{count} Dokumente gelöscht.")

if __name__ == "__main__":
    while True:
        print("\n=== RESTAURANT MANAGER (Bereich 3) ===")
        print("1: Bezirke auflisten")
        print("2: Top 3 Ratings")
        print("3: Nächstgelegenes zu 'Le Perigord'")
        print("4: Suchen & Bewerten")
        print("5: Restaurant hinzufügen")
        print("6: Restaurant löschen")
        print("0: Beenden")
        
        cmd = input("Wahl: ")
        if cmd == "1": list_boroughs()
        elif cmd == "2": top_3_restaurants()
        elif cmd == "3": nearest_to_perigord()
        elif cmd == "4": search_and_rate()
        elif cmd == "5": add_restaurant()
        elif cmd == "6": delete_restaurant()
        elif cmd == "0": break