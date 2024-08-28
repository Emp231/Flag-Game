import matplotlib
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import os
import random

class ImageRevealer:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Image Revealer")
        
        self.image = Image.open(image_path)
        self.image_width, self.image_height = self.image.size
        
        self.canvas = tk.Canvas(root, width=self.image_width, height=self.image_height)
        self.canvas.pack()
        
        self.reveal_width = 100
        self.reveal_height = 100

        self.regions_to_reveal = [
            (0, 0, 100, 100),  # Top-left corner
            (self.image_width - 100, self.image_height - 100, self.image_width, self.image_height),  # Bottom-right corner
            (self.image_width // 2 - 50, 0, self.image_width // 2 + 50, 100),  # Top-center
            (0, self.image_height // 2 - 50, 100, self.image_height // 2 + 50),  # Left-center
        ]
        self.image_refs = []

        self.current_region_index = 0
        self.gen_reveal()
        self.update_image()

        self.reveal_button = tk.Button(root, text="Reveal More", command=self.reveal_more)
        self.reveal_button.pack()
    
    def update_image(self):
        region = self.regions_to_reveal[self.current_region_index]
        
        cropped_image = self.image.crop(region)
        
        photo = ImageTk.PhotoImage(cropped_image)
        
        x_offset, y_offset = region[0], region[1]
        
        self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=photo)
        
        self.image_refs.append(photo)



    def reveal_more(self):
        if self.current_region_index < len(self.regions_to_reveal) - 1:
            self.current_region_index += 1

            self.update_image()
        else:
            self.reveal_button.config(state=tk.DISABLED)  # Disable button when all regions are revealed

    def gen_reveal(self):
        x_pos = 0
        y_pos = 0
        while True:
          x_pos = random.randint(0, self.image_width)
          y_pos = random.randint(0, self.image_height)

          cond = True
          for point in self.regions_to_reveal:
            if rectangles_overlap(point[0], point[1], x_pos, y_pos, self.reveal_width, self.reveal_height):
                cond = False
                break
          
          if cond:
              break
        
        return x_pos, y_pos

    
def rectangles_overlap(x1, y1, x2, y2, width, height):
    if x1 + width <= x2 or x2 + width <= x1:
        return False
    
    if y1 + height <= y2 or y2 + height <= y1:
        return False
    
    return True

# Main part of the code
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRevealer(root, "american-flag-clip-art-45.png")
    print(app.gen_reveal())
    root.mainloop()