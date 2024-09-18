import tkinter as tk
from PIL import Image, ImageTk
from map_generation import MapGeneration
from character import Character

class TerrainMapApp:
    def __init__(self, root, size=20, tile_size=32):
        self.size = size
        self.tile_size = tile_size
        self.root = root
        self.root.title("ASCII Terrain Map with Controllable Character")

        # Create a canvas to draw the map
        self.canvas = tk.Canvas(self.root, width=self.size * tile_size, height=self.size * tile_size)
        self.canvas.pack()

        # Generate the terrain and ASCII map
        generated_map = MapGeneration(size=50)
        self.terrain = generated_map.generate_perlin_noise()
        self.ascii_map = generated_map.generate_ascii_map(self.terrain)
        
        # Initialize the character
        self.character = Character(self.size, self.canvas, self.ascii_map, self.terrain, "character_spritesheet.png", 24, 32, self.tile_size)

        # Draw the initial map with the character
        self.draw_map()
        
        # Bind arrow keys for movement
        self.root.bind('<Up>', self.move_up)
        self.root.bind('<Down>', self.move_down)
        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)

    def draw_map(self):
        """
        Draw the terrain map with images and the character.
        """
        for i, row in enumerate(self.ascii_map):
            for j, image in enumerate(row):
                self.canvas.create_image(j * self.tile_size, i * self.tile_size, anchor=tk.NW, image=image)

        # Draw the character on top
        self.character.draw_character()
        
    def move_up(self, event):
        self.character.move('up')

    def move_down(self, event):
        self.character.move('down')

    def move_left(self, event):
        self.character.move('left')
        
    def move_right(self, event):
        self.character.move('right')

def display_image_map(size=20):
    """
    Display the terrain map with a controllable character.
    """
    root = tk.Tk()
    app = TerrainMapApp(root, size)
    root.mainloop()

# Display the terrain map with a controllable character
display_image_map(size=50)
