import tkinter as tk
from PIL import Image, ImageTk

class Character:
    def __init__(self, size, tile_size, canvas, isometric_map, terrain, sprite_sheet_path, sprite_width, sprite_height, tile_width, tile_height, start_x=0, start_y=0):
        self.size = size
        self.tile_size = tile_size
        self.canvas = canvas
        self.isometric_map = isometric_map
        self.terrain = terrain
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.character_x = start_x
        self.character_y = start_y
        self.character_direction = 'down'
        self.current_frame = 0
        self.animation_running = False
        self.last_position = None
        
        # Inventory system (list to hold items)
        self.inventory = []
        
        # Load the character sprite sheet and extract 8 frames per direction
        self.character_sprites = self.load_character_sprites(sprite_sheet_path, sprite_width, sprite_height)

    def load_character_sprites(self, sprite_sheet_path, sprite_width, sprite_height):
        """
        Load the character sprite sheet and extract 8 frames for each direction (down, left, right, up).
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
    
    def grid_to_isometric(self, x, y):
        """
        Convert (x, y) grid coordinates to isometric coordinates.
        """
        iso_x = (x - y) * (self.tile_width // 2)
        iso_y = (x + y) * (self.tile_height // 2)
        return iso_x, iso_y
    
    def draw_character(self):
        """
        Draw the character at the current position on the canvas.
        """
        if self.last_position:
            # Only clear the previous character position
            last_x, last_y = self.last_position
            
            # Find the previous tile's isometric coordinates from the map
            for tile in self.isometric_map:
                if tile['x'] == last_x and tile['y'] == last_y:
                    self.canvas.create_image(tile['x'], tile['y'], anchor=tk.NW, image=tile['image'])
                    break
                
             # Find the current tile's isometric coordinates
        current_tile = None
        for tile in self.isometric_map:
            if tile['x'] == self.character_x and tile['y'] == self.character_y:
                current_tile = tile
                break

        if current_tile:
            # Draw the character on the canvas at the isometric tile's position
            character_image = self.character_sprites[self.character_direction][self.current_frame]
            self.canvas.create_image(current_tile['x'], current_tile['y'], anchor='nw', image=character_image)
            self.last_position = (self.character_x, self.character_y)
            
    def animate_character(self):
        """
        Animate the character by cycling through frames.
        """
        self.current_frame = (self.current_frame + 1) % 8 # Cycle through 8 frames
        self.draw_character()
        
        if self.animation_running:
            self.canvas.after(100, self.animate_character) # 100 ms delay for each frame
            
    def start_animation(self):
        """
        Start the animation and ensure it stops after a short duration
        """
        if not self.animation_running:
            self.animation_running = True 
            self.animate_character() 
            
        # Automatically stop animation after a short delay
        self.canvas.after(800, self.stop_animation) # Stop after 800 ms
        
    def stop_animation(self):
        """
        Stop the character animation and reset the frame.
        """
        self.animation_running = False 
        self.current_frame = 0
        self.draw_character()
        
    def is_walkable(self, x, y):
        """
        Check if the tile at (x, y) is walkable. A tile is walkable if it is not water.
        """
        if 0 <= x < self.size and 0 <= y < self.size:
            elevation = self.terrain[y, x]
            return elevation >= 0.2 and elevation < 0.8  # Walkable if elevation is greater than or equal to 0.2 (not water)
        return False

        
    def move(self, direction):
        """
        Move the character in the given direction, if the target tile is walkable.
        Also, scroll the canvas if the character is near the edge of the visible area.
        """
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Determine the amount of tiles visible on the canvas
        visible_x_tiles = canvas_width // self.tile_size
        visible_y_tiles = canvas_height // self.tile_size
        
        # Scroll area threshold: how close to the edge the character must be before scrolling
        scroll_threshold_x = visible_x_tiles // 4
        scroll_threshold_y = visible_y_tiles // 4
        
        # Move the character and update it's direction
        if direction == 'up' and self.character_y > 0 and self.is_walkable(self.character_x, self.character_y - 1):
            self.character_y -= 1
            self.character_direction = 'up'
        elif direction == 'down' and self.character_y < self.canvas.winfo_height() - 1 and self.is_walkable(self.character_x, self.character_y + 1):
            self.character_y += 1
            self.character_direction = 'down'
        elif direction == 'left' and self.character_x > 0 and self.is_walkable(self.character_x - 1, self.character_y):
            self.character_x -= 1
            self.character_direction = 'left'
        elif direction == 'right' and self.character_x < self.canvas.winfo_width() - 1 and self.is_walkable(self.character_x + 1, self.character_y):
            self.character_x += 1
            self.character_direction = 'right'
            
        self.start_animation()
        
        self.center_view()
        
    def scroll_map(self, threshold_x, threshold_y):
        """
        Scroll the canvas when the character approaches the edge of the visible area.
        :param threshold_x: Horizontal distance from the edge of the canvas before scrolling starts
        :param threshold_y: Vertical distance from the edge of the canvas before scrolling starts
        """
        # Get current visible region in terms of tile positions
        canvas_left = self.canvas.canvasx(0) // self.tile_size
        canvas_right = (self.canvas.canvasx(self.canvas.winfo_width()) // self.tile_size)
        canvas_top = self.canvas.canvasy(0) // self.tile_size
        canvas_bottom = (self.canvas.canvasy(self.canvas.winfo_height()) // self.tile_size)
        
        # Scroll horizontally if character is near the left or right edge of the visible area
        if self.character_x < canvas_left + threshold_x:
            self.canvas.xview_scroll(-1, "units") # Scroll left
        elif self.character_x > canvas_right - threshold_x:
            self.canvas.xview_scroll(1, "units") # Scroll right
            
        # Scroll vertically if character is near the top or bottom edge of the visible area
        if self.character_y < canvas_top + threshold_y:
            self.canvas.yview_scroll(-1, "units") # Scroll up
        elif self.character_y > canvas_bottom - threshold_y:
            self.canvas.yview_scroll(1, "units") # Scroll down
            
    def center_view(self):
        """
        Center the canvas view over the character or map.
        This method centers the character in the middle of the canvas if possible.
        """
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Calculate character pixel position on the canvas
        character_pixel_x = self.character_x * self.tile_size
        character_pixel_y = self.character_y * self.tile_size
        
        # Get half the canvas size to calculate the center point
        half_canvas_width = canvas_width // 2
        half_canvas_height = canvas_height // 2
        
        # Calculate the new view position to center the character
        new_view_x = character_pixel_x - half_canvas_width
        new_view_y = character_pixel_y - half_canvas_height
        
        # Scroll the canvas to center the character (adjust scroll region)
        self.canvas.xview_moveto(new_view_x / (self.size * self.tile_size))
        self.canvas.yview_moveto(new_view_y / (self.size * self.tile_size))
        