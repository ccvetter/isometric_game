import numpy as np
from PIL import Image, ImageTk
from noise import pnoise2
from utilities import save_terrain_images

def generate_perlin_noise(size, scale=10, octaves=6, persistence=0.5, lacunarity=2.0):
    """
    Generate a 2D numpy array of Perlin noise values for terrain generation.
    
    :param size: The size of the map (size x size)
    :param scale: Controls the zoom level of the Perlin noise
    :param octaves: Number of levels of detail
    :param persistence: Amplitude multiplier for each octave
    :param lacunarity: Frequency multiplier for each octave
    :return: 2D numpy array of terrain heights
    """
    noise_map = np.zeros((size, size))

    for y in range(size):
        for x in range(size):
            noise_map[y][x] = pnoise2(x / scale,
                                      y / scale,
                                      octaves=octaves,
                                      persistence=persistence,
                                      lacunarity=lacunarity,
                                      repeatx=size,
                                      repeaty=size,
                                      base=0)

    # Normalize values between 0 and 1
    min_val = np.min(noise_map)
    max_val = np.max(noise_map)
    noise_map = (noise_map - min_val) / (max_val - min_val)

    return noise_map

def generate_isometric_map(size, noise_map, terrain_image_map, tile_width, tile_height):
    """
    Generate a 2D array map where each terrain height corresponds to an image from the sprite sheet.
    
    :param size: The size of the map
    :param noise_map: 2D array of Perlin noise values representing the terrain
    :param terrain_image_map: Dictionary of terrain images generated from the sprite sheet
    :return: A 2D array representing the map with corresponding terrain images
    """
    isometric_map = []
    map_text = []

    for y in range(size):
        for x in range(size):
            elevation = noise_map[y][x]

            # Ensure proper separation of elevation values for different terrain types
            if elevation < 0.2:
                tile_image = terrain_image_map['water']
                map_text.append('water')
            elif 0.2 <= elevation < 0.4:
                tile_image = terrain_image_map['plains']
                map_text.append('plains')
            elif 0.4 <= elevation < 0.6:
                tile_image = terrain_image_map['hills']
                map_text.append('hills')
            elif 0.6 <= elevation < 0.8:
                tile_image = terrain_image_map['mountains']
                map_text.append('mountains')
            else:
                tile_image = terrain_image_map['high_peaks']
                map_text.append('high_peaks')

            # Convert (x, y) grid coordinates to isometric coordinates
            iso_x = (x - y) * (tile_width // 2)
            iso_y = (x + y) * (tile_height // 2)
            
            # Store tile image and its isometric coordinates
            isometric_map.append({
                'image': tile_image,
                'x': iso_x,
                'y': iso_y
            })
    print(map_text)
    return isometric_map

def create_terrain_image_map():
    """
    Create a terrain image map by slicing the sprite sheet into tiles.
    """
    water_file = Image.open("textures/map_tiles/tile_104.png")
    plains_file = Image.open("textures/map_tiles/tile_005.png")
    hills_file = Image.open("textures/map_tiles/tile_084.png")
    mountains_file = Image.open("textures/map_tiles/tile_050.png")
    high_peaks_file = Image.open("textures/map_tiles/tile_018.png")
    terrain_image_map = {
        'water': ImageTk.PhotoImage(water_file),
        'plains': ImageTk.PhotoImage(plains_file),
        'hills': ImageTk.PhotoImage(hills_file),
        'mountains': ImageTk.PhotoImage(mountains_file),
        'high_peaks': ImageTk.PhotoImage(high_peaks_file)
    }
        
    return terrain_image_map

def slice_spritesheet(sprite_sheet, tile_size):
    """
    Create a terrain image map by slicing the sprite sheet into tiles.
    
    Args:
        sprite_sheet (Image): The loaded sprite sheet image.
        tile_size (int): The size of each tile (assuming square tiles).
    
    Returns:
        dict: A dictionary where keys are (row, col) tuples and values are the corresponding tile images.
    """
    # Calculate the number of tiles in both dimensions
    tiles_x = sprite_sheet.width // tile_size
    tiles_y = sprite_sheet.height // tile_size

    # Create a dictionary to store the terrain images
    terrain_image_map = {}

    # Slice the sprite sheet into tiles and store them in the map
    for i in range(tiles_y):
        for j in range(tiles_x):
            # Crop the sprite sheet to get the tile
            tile = sprite_sheet.crop((
                j * tile_size,   # left
                i * tile_size,   # upper
                (j + 1) * tile_size,  # right
                (i + 1) * tile_size   # lower
            ))

            # Store each tile in the terrain map with the (i, j) key
            terrain_image_map[(i, j)] = tile
    
    save_terrain_images(terrain_image_map, "alt_terrain", save_directory="./textures")
