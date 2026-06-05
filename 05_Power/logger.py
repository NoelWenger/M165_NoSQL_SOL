import time
from pymongo import MongoClient
from power import Power

client = MongoClient("mongodb+srv://Wengsi:1234@cluster0.ghns1ap.mongodb.net/?appName=Cluster0")
db = client["monitor_db"]
col = db["power_logs"]

def run_logger():
    print("Starte Monitoring... (Strg+C zum Beenden)")
    while True:
        log = Power()
        col.insert_one(log.__dict__)
        print(f"Log gespeichert: CPU {log.cpu}%")

        if col.count_documents({}) > 10000:
            oldest = col.find().sort("timestamp", 1).limit(1)
            col.delete_one({"_id": oldest[0]["_id"]})
            print("Ältestes Log gelöscht.")

        time.sleep(1)

if __name__ == "__main__":
    run_logger()