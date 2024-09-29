import os 

def save_terrain_images(terrain_image_map, prefix, save_directory="textures"):
    """
    Save the sliced sprite sheet images as individual image files.
    
    :param terrain_image_map: Dictionary of terrain images from the sprite sheet.
    :param save_directory: Directory to save the sliced images.
    """
    # Create directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
        
    for (row, col), image in terrain_image_map.items():
        # Define the file name for each tile
        file_name = f"{prefix}_{row}_{col}.png"
        # Full path where the image will be saved
        save_path = os.path.join(save_directory, file_name)
        # Save the image
        image.save(save_path)
        
