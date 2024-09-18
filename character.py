from PIL import Image, ImageTk

class Character:
    def __init__(self, size, canvas, ascii_map, terrain, sprite_sheet_path, sprite_width, sprite_height, tile_size, start_x=0, start_y=0):
        self.size = size
        self.canvas = canvas
        self.ascii_map = ascii_map
        self.terrain = terrain
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self.tile_size = tile_size
        self.character_x = start_x
        self.character_y = start_y
        self.character_direction = 'down'
        self.current_frame = 0
        self.animation_running = False
        self.last_position = None
        
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
    
    def draw_character(self):
        """
        Draw the character at the current position on the canvas.
        """
        if self.last_position:
            # Only clear the previous character position
            last_x, last_y = self.last_position
            tile_image = self.ascii_map[last_y][last_x]
            self.canvas.create_image(last_x * self.tile_size, last_y * self.tile_size, anchor='nw', image=tile_image)
            
        # Draw the character on the canvas at the current position
        character_image = self.character_sprites[self.character_direction][self.current_frame]
        self.canvas.create_image(self.character_x * self.tile_size, self.character_y * self.tile_size, anchor='nw', image=character_image)
        
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
            return elevation >= -0.06 and elevation < 0.4  # Walkable if elevation is greater than or equal to 0.2 (not water)
        return False

        
    def move(self, direction):
        """
        Move the character in the given direction, if the target tile is walkable.
        """
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
        