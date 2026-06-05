import os
from dotenv import load_dotenv
from dao_joke import Dao_joke
from joke import Joke

load_dotenv()
uri = os.getenv("MONGO_URI")

dao = Dao_joke(uri, "fun_db", "jokes")

mein_witz = Joke("Warum können Geister so schlecht lügen? Weil man durch sie hindurchsehen kann!", ["Flachwitz", "Grusel"], "Noel")
result = dao.insert(mein_witz)
print(f"Witz eingefügt mit ID: {result.inserted_id}")

jokes = dao.get_category("Flachwitz")
for j in jokes:
    print(f"Gefunden: {j.text} von {j.author}")