import tkinter as tk
from PIL import Image
from map_generation import generate_perlin_noise, generate_isometric_map, create_terrain_image_map
from character import Character
from inventory import Inventory

class TerrainMapApp:
    def __init__(self, root, size=20, tile_size=32, sprite_sheet_path="tileset/spritesheet.png"):
        self.size = size
        self.tile_size = tile_size
        self.tile_width = 32 # Isometric tile width
        self.tile_height = 32 # Isometric tile height
        self.root = root
        self.root.title("Terrain Map with Controllable Character")
        
        # self.terrain_spritesheet = Image.open(sprite_sheet_path)
        # self.terrain_spritesheet_alt = Image.open("textures/hyptosis_tile-art-batch-1.png")
        
        # Create a canvas with scrollbars
        self.canvas = tk.Canvas(self.root, width=self.size * self.tile_size, height=self.size * self.tile_size, scrollregion=(0, 0, self.size * self.tile_size * 2, self.size * self.tile_size * 2))
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbars
        x_scrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        x_scrollbar.config(command=self.canvas.yview)
        
        y_scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        y_scrollbar.config(command=self.canvas.yview)
        
        # Configure canvas scroll commands
        self.canvas.config(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

        # Generate the terrain and map
        self.terrain = generate_perlin_noise(self.size)
        self.terrain_image_map = create_terrain_image_map()
        self.isometric_map = generate_isometric_map(self.size, self.terrain, self.terrain_image_map, self.tile_width, self.tile_height)

        # Initialize the character
        self.character = Character(self.size, self.tile_size, self.canvas, self.isometric_map, self.terrain, "character_spritesheet.png", 24, 32, self.tile_width, self.tile_height)

        # Create an inventory for the character
        self.character.inventory = Inventory(self.root)
        
        # Add some items to the character's inventory (example items)
        self.character.inventory.add_item("Sword", 1)
        self.character.inventory.add_item("Health Potion", 3)
        self.character.inventory.add_item("Shield", 1)
        
        # Draw the initial map with the character
        self.draw_isometric_map(self.isometric_map)
        
        # Bind arrow keys for movement
        self.root.bind('<Up>', self.move_up)
        self.root.bind('<Down>', self.move_down)
        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)
        
        # Bind 'i' key to toggle inventory overlay
        self.root.bind('i', self.character.inventory.toggle_inventory)
    
    def draw_isometric_map(self, isometric_map):
        """
        Draw the terrain map with images and the character.
        """
        # Iterate over the ASCII map and use the terrain images
        self.image_references = []  # Store references to images to prevent garbage collection

        for tile in isometric_map:
            # Add the image to the canvas at it's isometric coordinates
            tile_image = tile['image']
            x = tile['x']
            y = tile['y']
            self.canvas.create_image(x, y, anchor=tk.NW, image=tile_image)
            
            # Keep a reference to prevent the image from being garbage collected
            self.image_references.append(tile_image)
                
        # Draw the character on top
        self.character.draw_character()
        
        # Center the view after drawing the character
        self.character.center_view()
        
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
display_image_map(size=60)
