import numpy as np
from noise import pnoise2
from PIL import Image, ImageTk

class MapGeneration:
    def __init__(self, size=20):
        self.size = size
        self.tile_size = 32
        
        # Cache images to avoid redundant loading
        self.water_image = ImageTk.PhotoImage(Image.open("water.png").resize((self.tile_size, self.tile_size)))
        self.plains_image = ImageTk.PhotoImage(Image.open("plains.png").resize((self.tile_size, self.tile_size)))
        self.hills_image = ImageTk.PhotoImage(Image.open("hills.png").resize((self.tile_size, self.tile_size)))
        self.mountains_image = ImageTk.PhotoImage(Image.open("mountains.png").resize((self.tile_size, self.tile_size)))
        self.high_peaks_image = ImageTk.PhotoImage(Image.open("high_peaks.png").resize((self.tile_size, self.tile_size)))

    def generate_perlin_noise(self, scale=10, octaves=6, persistence=0.5, lacunarity=2.0):
        """
        Generate a Perlin noise terrain map with elevation.
        """
        terrain = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(self.size):
                noise_value = pnoise2(i / scale, 
                                        j / scale, 
                                        octaves=octaves, 
                                        persistence=persistence, 
                                        lacunarity=lacunarity, 
                                        repeatx=self.size, 
                                        repeaty=self.size, 
                                        base=0)
                terrain[i, j] = noise_value #(noise_value + 1) / 2  # Normalize to [0, 1]
        return terrain

    def elevation_to_image(self, elevation):
        """
        Convert elevation value to an terrain image and return the corresponding tag.
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

    def generate_ascii_map(self, terrain):
        """
        Generate an ASCII map based on the terrain elevation with corresponding tags.
        """
        ascii_map = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                elevation = terrain[i, j]
                image = self.elevation_to_image(elevation)
                row.append(image)
            ascii_map.append(row)
        return ascii_map
