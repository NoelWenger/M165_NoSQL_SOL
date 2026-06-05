from PIL import Image, ImageDraw
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["sample_restaurants"]
col = db["neighborhoods"]

MIN_X, MAX_X = -74.3, -73.7
MIN_Y, MAX_Y = 40.5, 41.0
WIDTH, HEIGHT = 1000, 1000

def get_pixel(long, lat):
    x = int((long - MIN_X) / (MAX_X - MIN_X) * WIDTH)
    # Y-Achse wird umgedreht, da Pixel (0,0) oben links ist
    y = int((1 - (lat - MIN_Y) / (MAX_Y - MIN_Y)) * HEIGHT)
    return (x, y)

def draw_polygon(draw, coords, color):
    pixel_coords = []
    for c in coords:
        long = c[0]
        lat = c[1]
        
        pixel_coords.append(get_pixel(long, lat))
    
    if len(pixel_coords) > 2:
        draw.polygon(pixel_coords, outline=color, fill=None)

def visualize_neighborhoods(single_only=False):
    im = Image.new(mode="RGB", size=(WIDTH, HEIGHT), color="white")
    draw = ImageDraw.Draw(im)

    if single_only:
        poly = col.find_one()
        if poly:
            coords = poly["geometry"]["coordinates"][0]
            draw_polygon(draw, coords, "blue")
    else:
        for poly in col.find():
            try:
                coords = poly["geometry"]["coordinates"][0]
                draw_polygon(draw, coords, "black")
            except Exception:
                continue

    im.show()
    im.save("neighborhoods_map.png")
    print("Grafik wurde gespeichert als 'neighborhoods_map.png'")

if __name__ == "__main__":
    visualize_neighborhoods(single_only=False)