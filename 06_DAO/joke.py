class Joke:
    def __init__(self, text, category, author, _id=None):
        self._id = _id
        self.text = text
        self.category = category  # Liste von Kategorien
        self.author = author