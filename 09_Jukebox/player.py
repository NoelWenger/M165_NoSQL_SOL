from collections import deque

class Player:
    def __init__(self, dao):
        self.dao = dao
        self.playlist = deque()

    def search_and_add(self):
        print("Suche (leer lassen zum Ignorieren):")
        name = input("Name: ")
        artist = input("Interpret: ")
        results = self.dao.search(name=name, artist=artist)
        
        for i, song in enumerate(results):
            print(f"[{i}] {song['name']} von {song['artist']}")
        
        idx = int(input("Song Nummer zur Playlist hinzufügen: "))
        self.playlist.append(results[idx])
        print("Song hinzugefügt.")

    def play(self):
        if not self.playlist:
            song = self.dao.get_random()
            print(f"Spiele zufälligen Song: {song['name']}")
        else:
            song = self.playlist.popleft()
            print(f"Spiele aus Playlist: {song['name']}")

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from dao_jukebox import DaoJukebox
    
    load_dotenv()
    dao = DaoJukebox(os.getenv("MONGO_URI"))
    p = Player(dao)
    
    while True:
        print("\n=== JUKEBOX PLAYER ===")
        print("1: Song suchen & zur Playlist hinzufügen")
        print("2: Playlist abspielen (FIFO / Zufall)")
        print("3: Aktuelle Warteschlange anzeigen")
        print("0: Beenden")
        choice = input("Wahl: ")
        
        if choice == "1":
            try:
                p.search_and_add()
            except Exception as e:
                print(f"Fehler: {e}")
        elif choice == "2":
            p.play()
        elif choice == "3":
            if not p.playlist:
                print("Die Playlist ist leer (beim nächsten Abspielen wird ein zufälliger Song gewählt).")
            else:
                print("\nWarteschlange:")
                for i, song in enumerate(p.playlist):
                    print(f" - [{i+1}] {song['name']} von {song['artist']}")
        elif choice == "0":
            break