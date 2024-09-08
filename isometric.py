import tkinter as tk
import numpy as np
from noise import pnoise2
from PIL import Image, ImageTk

class TerrainMapApp:
    def __init__(self, root, size=20, tile_size=32):
        self.size = size
        self.tile_size = tile_size
        self.root = root
        self.root.title("ASCII Terrain Map with Controllable Character")

        # Cache images to avoid redundant loading
        self.water_image = ImageTk.PhotoImage(Image.open("water.png").resize((tile_size, tile_size)))
        self.plains_image = ImageTk.PhotoImage(Image.open("plains.png").resize((tile_size, tile_size)))
        self.hills_image = ImageTk.PhotoImage(Image.open("hills.png").resize((tile_size, tile_size)))
        self.mountains_image = ImageTk.PhotoImage(Image.open("mountains.png").resize((tile_size, tile_size)))
        self.high_peaks_image = ImageTk.PhotoImage(Image.open("high_peaks.png").resize((tile_size, tile_size)))

        # Load character sprite sheet and extract individual frames
        self.character_sprites = self.load_character_sprites("character_spritesheet.png", 24, 32)

        # Character initial position
        self.character_x = 0
        self.character_y = 0
        self.character_direction = 'down'
        self.current_frame = 0
        self.animation_running = False
        self.last_position = None
        
        # Create a canvas to draw the map
        self.canvas = tk.Canvas(self.root, width=self.size * tile_size, height=self.size * tile_size)
        self.canvas.pack()

        # Generate the terrain and ASCII map
        self.terrain = self.generate_perlin_noise(size)
        self.ascii_map = self.generate_ascii_map(size, self.terrain)

        # Draw the initial map with the character
        self.draw_map()

        # Bind arrow keys for movement
        self.root.bind('<Up>', self.move_up)
        self.root.bind('<Down>', self.move_down)
        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)
        # self.root.bind('<KeyRelease>', self.stop_animation())
        
    def load_character_sprites(self, sprite_sheet_path, sprite_width, sprite_height):
        """
        Load the character sprite sheet and extract 8 frames for each direction.

        :param sprite_sheet_path: Path to the sprite sheet image.
        :param width: Width of a single sprite frame.
        :param height: Height of a single sprite frame.
        :return: Dictionary with lists of 8 sprites for each direction.
        """
        sprite_sheet = Image.open(sprite_sheet_path)
        sprites = {
            'down': [],
            'up': [],
            'left': [],
            'right': []
        }
        
        for i, direction in enumerate(sprites.keys()):
            for frame in range(8):
                x = frame * sprite_width
                y = i * sprite_height
                sprite = ImageTk.PhotoImage(sprite_sheet.crop((x, y, x + sprite_width, y + sprite_height)))
                sprites[direction].append(sprite)

        return sprites

    def generate_perlin_noise(self, size, scale=10, octaves=6, persistence=0.5, lacunarity=2.0):
        """
        Generate a Perlin noise terrain map with elevation.
        """
        terrain = np.zeros((size, size))
        for i in range(size):
            for j in range(size):
                noise_value = pnoise2(i / scale, 
                                      j / scale, 
                                      octaves=octaves, 
                                      persistence=persistence, 
                                      lacunarity=lacunarity, 
                                      repeatx=size, 
                                      repeaty=size, 
                                      base=0)
                terrain[i, j] = noise_value #(noise_value + 1) / 2  # Normalize to [0, 1]
        return terrain

    def elevation_to_image(self, elevation):
        """
        Convert elevation value to an ASCII symbol and return the corresponding tag.
        """
        if elevation < -0.06:
            return self.water_image  # Water
        elif elevation < 0.15:
            return self.plains_image  # Plains
        elif elevation < 0.3:
            return self.hills_image  # Hills
        elif elevation < 0.4:
            return self.mountains_image  # Mountains
        else:
            return self.high_peaks_image  # High peaks

    def generate_ascii_map(self, size, terrain):
        """
        Generate an ASCII map based on the terrain elevation with corresponding tags.
        """
        ascii_map = []
        for i in range(size):
            row = []
            for j in range(size):
                elevation = terrain[i, j]
                image = self.elevation_to_image(elevation)
                row.append(image)
            ascii_map.append(row)
        return ascii_map

    def draw_map(self):
        """
        Draw the terrain map with images and the character.
        """
        if self.last_position:
            # Only clear the previous character position
            last_x, last_y = self.last_position
            tile_image = self.ascii_map[last_y][last_x]
            self.canvas.create_image(last_x * self.tile_size, last_y * self.tile_size, anchor=tk.NW, image=tile_image)
        else:
            # Initial full map draw
            for i, row in enumerate(self.ascii_map):
                for j, image in enumerate(row):
                     self.canvas.create_image(j * self.tile_size, i * self.tile_size, anchor=tk.NW, image=image)

        # Draw the character on top
        character_image = self.character_sprites[self.character_direction][self.current_frame]
        self.canvas.create_image(self.character_x * self.tile_size, self.character_y * self.tile_size, anchor=tk.NW, image=character_image)
        
        # Cache the current character position for next frame
        self.last_position = (self.character_x, self.character_y)
        
    def is_walkable(self, x, y):
        """
        Check if the tile at (x, y) is walkable. A tile is walkable if it is not water.
        """
        if 0 <= x < self.size and 0 <= y < self.size:
            elevation = self.terrain[y, x]
            return elevation >= -0.06 and elevation < 0.4  # Walkable if elevation is greater than or equal to 0.2 (not water)
        return False

    def animate_character(self):
        """
        Animate the character by cycling through the frames.
        """
        self.current_frame = (self.current_frame + 1) % 8 # Cycle through the 8 frames
        self.draw_map()
        
        if self.animation_running:
            self.root.after(100, self.animate_character) # 100 ms delay for animation frame
        
    def start_animation(self):
        if not self.animation_running:
            self.animation_running = True
            self.animate_character()
            
        self.root.after(200, self.stop_animation)
            
    def stop_animation(self):
        self.animation_running = False
        self.current_frame = 0 # Reset frame after stopping
        self.draw_map()
        
    def move_up(self, event):
        """
        Move the character up.
        """
        if self.character_y > 0 and self.is_walkable(self.character_x, self.character_y - 1):
            self.character_y -= 1
            self.character_direction = 'up'
            self.start_animation()

    def move_down(self, event):
        """
        Move the character down.
        """
        if self.character_y < self.size - 1 and self.is_walkable(self.character_x, self.character_y + 1):
            self.character_y += 1
            self.character_direction = 'down'
            self.start_animation()

    def move_left(self, event):
        """
        Move the character left.
        """
        if self.character_x > 0 and self.is_walkable(self.character_x - 1, self.character_y):
            self.character_x -= 1
            self.character_direction = 'left'
            self.start_animation()

    def move_right(self, event):
        """
        Move the character right.
        """
        if self.character_x < self.size - 1 and self.is_walkable(self.character_x + 1, self.character_y):
            self.character_x += 1
            self.character_direction = 'right'
            self.start_animation()

def display_image_map(size=20):
    """
    Display the terrain map with a controllable character.
    """
    root = tk.Tk()
    app = TerrainMapApp(root, size)
    root.mainloop()

# Display the terrain map with a controllable character
display_image_map(size=50)
