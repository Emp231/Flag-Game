import matplotlib
import tkinter as tk
from PIL import Image, ImageTk, ImageOps
import os
import random
import math

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

        x_pos = random.randint(0, self.image_width)
        y_pos = random.randint(0, self.image_height)
        

        self.regions_to_reveal = [
          (x_pos, y_pos, self.reveal_width+x_pos, self.reveal_height + y_pos)
        ]

        print(self.regions_to_reveal[0])
        self.image_refs = []

        self.current_region_index = 0
        self.update_image()

        self.reveal_button = tk.Button(root, text="Reveal More", command=self.reveal_more)
        self.reveal_button.pack()

        self.guess_button = tk.Button(root, text="Guess", command=self.open_guess_window)
        self.guess_button.pack()
    
    def update_image(self):
        region = self.regions_to_reveal[len(self.regions_to_reveal) - 1]
        
        cropped_image = self.image.crop(region)
        
        photo = ImageTk.PhotoImage(cropped_image)
        
        x_offset, y_offset = region[0], region[1]
        
        self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=photo)
        
        self.image_refs.append(photo)



    def reveal_more(self):
        if len(self.regions_to_reveal) < 5:
            x_pos, y_pos = self.gen_reveal()

            self.regions_to_reveal.append((x_pos, y_pos, self.reveal_width+x_pos, self.reveal_height+y_pos))
            self.update_image()
        else:
            self.reveal_button.config(state=tk.DISABLED)
    def gen_reveal(self):
        x_pos = 0
        y_pos = 0
        while True:
          x_pos = random.randint(0, self.image_width)
          y_pos = random.randint(0, self.image_height)

          cond = True
          for point in self.regions_to_reveal:
            if rectangles_overlap(point[0], point[1], x_pos, y_pos, self.reveal_width, self.reveal_height) or (far_enough(point[0], point[1], x_pos, y_pos, self.reveal_width, self.reveal_height) < 300):
                cond = False
                break
          
          if cond:
              break
        
        return x_pos, y_pos
    
    def open_guess_window(self):
        guess_window = tk.Toplevel(self.root)
        guess_window.title("Guess Window")

        guess_image = Image.open("World_Map.png")
        guess_photo = ImageTk.PhotoImage(guess_image)

        guess_canvas = tk.Canvas(guess_window, width=guess_image.width, height=guess_image.height)
        guess_canvas.pack()
        guess_canvas.create_image(0, 0, anchor=tk.NW, image=guess_photo)

        self.pin_id = None
        self.guess_canvas = guess_canvas

        def on_click(event):
            if self.pin_id is not None:
                guess_canvas.delete(self.pin_id)
            
            x, y = event.x, event.y
            self.pin_id = guess_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", outline="black")

        guess_canvas.bind("<Button-1>", on_click)

        guess_window.image_refs = [guess_photo]

        def on_click(event):
            if self.pin_id is not None:
                guess_canvas.delete(self.pin_id)
            
            x, y = event.x, event.y
            self.pin_id = guess_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", outline="black")

        guess_canvas.bind("<Button-1>", on_click)

        guess_window.image_refs = [guess_photo]
    
def rectangles_overlap(x1, y1, x2, y2, width, height):
    if x1 + width <= x2 or x2 + width <= x1:
        return False
    
    if y1 + height <= y2 or y2 + height <= y1:
        return False
    
    return True

def far_enough(x1, y1, x2, y2, width, height):
    midx_1 = x1 + width/2
    midy_1 = y1 + height/2
    midx_2 = x2 + width/2
    midy_2 = y2 + height/2

    dist = math.sqrt((midx_2-midx_1)**2 + (midy_2 - midy_1)**2)
    return dist

# Main part of the code
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRevealer(root, "american-flag-clip-art-45.png")
    print(app.gen_reveal())
    root.mainloop()