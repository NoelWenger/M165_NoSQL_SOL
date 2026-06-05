import matplotlib.pyplot as plt
from pymongo import MongoClient

client = MongoClient("mongodb+srv://Wengsi:1234@cluster0.ghns1ap.mongodb.net/")
col = client["monitor_db"]["power_logs"]

def show_graph():
    # Hole die letzten 100 Logs
    logs = list(col.find().sort("timestamp", -1).limit(100))
    logs.reverse() # Damit die Zeit links beginnt

    cpus = [l["cpu"] for l in logs]
    timestamps = [l["timestamp"] for l in logs]

    plt.plot(timestamps, cpus, label="CPU (%)")
    plt.xlabel("Zeit")
    plt.ylabel("Auslastung")
    plt.title("CPU Auslastung")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    show_graph()