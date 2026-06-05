import gridfs
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["photo_album_db"]
fs = gridfs.GridFS(db)

def save_photo(file_path, album_name):
    with open(file_path, 'rb') as f:
        file_id = fs.put(f, filename=os.path.basename(file_path), metadata={"album": album_name})
        print(f"Foto gespeichert mit ID: {file_id}")

def get_photos_by_album(album_name):
    files = fs.find({"metadata.album": album_name})
    for file in files:
        print(f"Lade: {file.filename}")
        data = file.read()
        with open(f"downloaded_{file.filename}", "wb") as f:
            f.write(data)
    print("Download abgeschlossen.")

if __name__ == "__main__":
    pass