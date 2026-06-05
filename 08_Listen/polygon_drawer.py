from PIL import Image, ImageDraw
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["sample_restaurants"]
col = db["neighborhoods"]

# Skalierung angepasst für New York Koordinaten
SCALE = 10000 
OFFSET_X = 740000 
OFFSET_Y = -400000

def draw_polygon(draw, coords, color):
    pixel_coords = []
    for c in coords:
        # Sicherstellen, dass c wirklich die zwei Zahlen [long, lat] sind
        long = c[0]
        lat = c[1]
        
        # Berechnung (Hier war das 'n' im Weg)
        x = int((long * SCALE) + OFFSET_X)
        y = int((lat * SCALE) + OFFSET_Y)
        
        pixel_coords.append((x, y))
    
    # Erst zeichnen, wenn genug Punkte da sind
    if len(pixel_coords) > 2:
        draw.polygon(pixel_coords, outline=color)

def visualize_neighborhoods(single_only=False):
    im = Image.new(mode="RGB", size=(1000, 1000), color="white")
    draw = ImageDraw.Draw(im)

    if single_only:
        poly = col.find_one()
        # Bei vielen GeoJSONs ist die Struktur: geometry -> coordinates -> [0]
        draw_polygon(draw, poly["geometry"]["coordinates"][0], "blue")
    else:
        for poly in col.find():
            try:
                coords = poly["geometry"]["coordinates"][0]
                draw_polygon(draw, coords, "black")
            except:
                continue # Überspringe Dokumente, die keine gültigen Koordinaten haben

    im.show()

if __name__ == "__main__":
    visualize_neighborhoods(single_only=False)