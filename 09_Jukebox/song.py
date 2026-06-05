class Song:
    def __init__(self, name, artist, album=None, genre=None, year=None, _id=None):
        self._id = _id
        self.name = name
        self.artist = artist
        self.album = album
        self.genre = genre
        self.year = year