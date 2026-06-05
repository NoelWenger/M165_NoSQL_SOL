from song import Song
from dao_jukebox import DaoJukebox
import os
from dotenv import load_dotenv

load_dotenv()
dao = DaoJukebox(os.getenv("MONGO_URI"))

def menu():
    while True:
        print("\n=== JUKEBOX MANAGEMENT ===")
        print("1: Song hinzufügen")
        print("2: Song ändern")
        print("3: Song löschen")
        print("0: Beenden")
        choice = input("Wahl: ")

        if choice == "1":
            name = input("Name: ")
            artist = input("Interpret: ")
            album = input("Album (optional): ")
            genre = input("Genre (optional): ")
            year = input("Jahr (optional): ")
            song = Song(name, artist, album, genre, year)
            dao.insert(song)
            print("Song gespeichert!")

        elif choice == "2":
            # 1. Suchen
            name = input("Suchbegriff für den zu ändernden Song (Name): ")
            results = dao.search(name=name)
            for i, s in enumerate(results):
                print(f"[{i}] {s['name']} - {s['artist']}")
            
            idx = int(input("Nummer wählen: "))
            new_name = input("Neuer Name: ")
            dao.update(results[idx]["_id"], {"name": new_name})
            print("Song aktualisiert.")

        elif choice == "3":
            name = input("Name des zu löschenden Songs: ")
            results = dao.search(name=name)
            for i, s in enumerate(results):
                print(f"[{i}] {s['name']}")
            
            idx = int(input("Nummer zum Löschen wählen: "))
            dao.delete(results[idx]["_id"])
            print("Song gelöscht.")

        elif choice == "0":
            break

if __name__ == "__main__":
    menu()