from pymongo import MongoClient
from bson import ObjectId

class DaoJukebox:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.col = self.client["jukebox_db"]["songs"]

    def insert(self, song):
        return self.col.insert_one(song.__dict__)

    def delete(self, song_id):
        return self.col.delete_one({"_id": ObjectId(song_id)})

    def update(self, song_id, new_data):
        return self.col.update_one({"_id": ObjectId(song_id)}, {"$set": new_data})

    def search(self, name=None, artist=None, album=None, genre=None):
        query = {}
        # Erstellt dynamisch einen Such-Query für Teilbegriffe (Regex "i")
        if name: query["name"] = {"$regex": name, "$options": "i"}
        if artist: query["artist"] = {"$regex": artist, "$options": "i"}
        if album: query["album"] = {"$regex": album, "$options": "i"}
        if genre: query["genre"] = {"$regex": genre, "$options": "i"}
        
        return list(self.col.find(query))

    def get_random(self):
        return self.col.aggregate([{"$sample": {"size": 1}}]).next()