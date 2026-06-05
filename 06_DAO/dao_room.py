from pymongo import MongoClient
from bson import ObjectId

class Dao_room:
    def __init__(self, connection_string, db_name="school", col_name="rooms"):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[col_name]

    def create(self, room):
        return self.collection.insert_one(room.__dict__)

    def read(self):
        return list(self.collection.find())

    def update(self, room_id, new_values):
        # Aktualisiert ein Dokument anhand der ID
        self.collection.update_one({"_id": ObjectId(room_id)}, {"$set": new_values})

    def delete(self, room_id):
        # Löscht ein Dokument anhand der ID
        self.collection.delete_one({"_id": ObjectId(room_id)})