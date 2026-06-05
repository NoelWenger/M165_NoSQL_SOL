from pymongo import MongoClient
from bson import ObjectId
import sys

uri = "mongodb+srv://Wengsi:1234@cluster0.ghns1ap.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)

def start_app():
    while True:
        print("\nDatabases")
        dbs = client.list_database_names()
        
        if not dbs:
            print("No Database")
            input("\nPress any button to return")
            continue
            
        for db_name in dbs:
            print(f" - {db_name}")

        while True:
            selected_db_name = input("\nSelect Database: ")
            if selected_db_name in dbs:
                break
            print(f"Error: Database '{selected_db_name}' not found. Please try again.")

        db = client[selected_db_name]
        col_list = db.list_collection_names()

        print(f"\n<{selected_db_name}>")
        print("\nCollections")
        
        if not col_list:
            print("No Collection")
            input("\nPress any button to return")
            continue

        for col_name in col_list:
            print(f" - {col_name}")

        while True:
            selected_col_name = input("\nSelect Collection: ")
            if selected_col_name in col_list:
                break
            print(f"Error: Collection '{selected_col_name}' not found. Please try again.")

        col = db[selected_col_name]
        cursor = col.find({}, {"_id": 1})
        doc_ids = [str(doc["_id"]) for doc in cursor]

        print(f"\n{selected_db_name}.{selected_col_name}")
        print("\nDocuments")
        
        if not doc_ids:
            print("No Document")
            input("\nPress any button to return")
            continue

        for d_id in doc_ids:
            print(f" - {d_id}")

        while True:
            selected_id_str = input("\nSelect Document: ")
            if selected_id_str in doc_ids:
                break
            print(f"Error: ID '{selected_id_str}' not found. Please try again.")

        document = col.find_one({"_id": ObjectId(selected_id_str)})
        
        print(f"\n{selected_db_name}.{selected_col_name}.{selected_id_str}\n")
        
        if document:
            for key, value in document.items():
                if key != "_id":
                    print(f"{key}: {value}")
        
        input("\nPress any button to return")

if __name__ == "__main__":
    try:
        start_app()
    except KeyboardInterrupt:
        print("\nApplikation beendet.")
        sys.exit()