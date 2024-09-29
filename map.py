import tkinter as tk
import geopandas as gpd
from shapely.geometry import Point
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

def get_country_from_coordinates(x, y, width, height):
    lon = (x / width) * 360 - 180 
    lat = 90 - (y / height) * 180  
    
    point = Point(lon, lat)  
    
    for country in world.itertuples():
        if country.geometry.contains(point):
            return country.name
    return "Unknown"

def on_map_click(event):
    x, y = event.x, event.y
    country = get_country_from_coordinates(x, y, img_width, img_height)
    
    print(f"Clicked at: ({x}, {y})")
    print(f"Country: {country}")
    clicked_countries.append(country)

clicked_countries = []

root = tk.Tk()
root.title("World Map Clicker")

map_image = Image.open("World_Map.png")
img_width, img_height = map_image.size
map_photo = ImageTk.PhotoImage(map_image)

map_label = tk.Label(root, image=map_photo)
map_label.pack()

map_label.bind("<Button-1>", on_map_click)

root.mainloop()