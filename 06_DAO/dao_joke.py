from pymongo import MongoClient
from bson import ObjectId
from joke import Joke

class Dao_joke:
    def __init__(self, connection_string, db_name, col_name):
        self.client = MongoClient(connection_string)
        self.collection = self.client[db_name][col_name]

    def insert(self, joke):
        return self.collection.insert_one(joke.__dict__)

    def get_category(self, category):
        query = {"category": category}
        cursor = self.collection.find(query)
        return [Joke(**doc) for doc in cursor]

    def delete(self, joke_id):
        return self.collection.delete_one({"_id": ObjectId(joke_id)})

    def update(self, joke_id, new_data):
        # new_data ist ein dict mit den Feldern, die sich ändern sollen
        return self.collection.update_one({"_id": ObjectId(joke_id)}, {"$set": new_data})