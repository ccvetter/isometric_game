import tkinter as tk
from PIL import Image, ImageTk 

class Enemy:
    def __init__(self, size, canvas, ascii_map, terrain, sprite_sheet_path, sprite_width, sprite_height, tile_size, start_x=0, start_y=0):
        self.size = size
        self.canvas = canvas
        self.ascii_map = ascii_map
        self.terrain = terrain
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.tile_size = tile_size
        self.enemy_x = start_x
        self.enemy_y = start_y
        self.enemy_direction = 'down'
        self.current_frame = 0
        self.animation_running = False
        self.last_position = None 
        
        self.enemy_sprites = self.load_enemy_sprites(sprite_sheet_path, sprite_width, sprite_height)
        
    def load_enemy_sprites(self, sprite_sheet_path, sprite_width, sprite_height):
        """
        Load the enemy sprite and extract 8 frames for each direction.
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
    
    def draw_enemy(self):
        """
        Draw the enemy at the current position on the canvas.
        """
        if self.last_position:
            # Only clear the previous enemy position
            last_x, last_y = self.last_position 
            tile_image = self.ascii_map[last_y][last_x]
            self.canvas.create_image(last_x * self.tile_size, last_y * self.tile_size, anchor=tk.NW, image=tile_image)
            
        # Draw the enemy on the canvas at the current position
        enemy_image = self.enemy_sprites[self.enemy_direction][self.current_frame]
        self.canvas.create_image(self.enemy_x * self.tile_size, self.enemy_y * self.tile_size, anchor=tk.NW, image=enemy_image)
       
        self.last_position = (self.enemy_x, self.enemy_y)
        
    def animate_enemy(self):
        """
        Animate the enemy by cycling through frames.
        """
        self.current_frame = (self.current_frame + 1) % 8 # Cycle through 8 frames
        self.draw_enemy()
        
        if self.animation_running:
            self.canvas.after(100, self.animate_enemy) # 100 ms delay for each frame
            
    def start_animation(self):
        """
        Start the animation and ensure it stops after a short duration
        """
        if not self.animation_running:
            self.animation_running = True
            self.animate_enemy
            
        # Automatically stop animation after a short delay
        self.canvas.after(800, self.stop_animation) # Stop after 800 ms
        
    def stop_animation(self):
        """
        Stop the enemy animation and reset the frame.
        """
        self.animation_running = False
        self.current_frame = 0
        self.draw_enemy()
        
    def is_walkable(self, x, y):
        """
        Check if the tile at (x, y) is walkable. A tile is walkable if it is not water.
        """
        if 0 <= x < self.size and 0 <= y < self.size:
            elevation = self.terrain[y, x]
            return elevation >= 0.2 and elevation < 0.8  # Walkable if elevation is not water
        return False

        
    def move(self, direction):
        """
        Move the enemy in the given direction, if the target tile is walkable.
        """
        if direction == 'up' and self.enemy_y > 0 and self.is_walkable(self.enemy_x, self.enemy_y - 1):
            self.enemy_y -= 1
            self.enemy_direction = 'up'
        elif direction == 'down' and self.enemy_y < self.canvas.winfo_height() - 1 and self.is_walkable(self.enemy_x, self.enemy_y + 1):
            self.enemy_y += 1
            self.enemy_direction = 'down'
        elif direction == 'left' and self.enemy_x > 0 and self.is_walkable(self.enemy_x - 1, self.enemy_y):
            self.enemy_x -= 1
            self.enemy_direction = 'left'
        elif direction == 'right' and self.enemy_x < self.canvas.winfo_width() - 1 and self.is_walkable(self.enemy_x + 1, self.enemy_y):
            self.enemy_x += 1
            self.enemy_direction = 'right'
            
        self.start_animation()