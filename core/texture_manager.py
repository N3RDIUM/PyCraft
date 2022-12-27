# imports
from os import listdir
from os.path import exists, isfile, join

import numpy as np
from OpenGL.GL import (GL_BGR, GL_CLAMP_TO_EDGE, GL_LINEAR, GL_RGBA, GL_RGBA8,
                       GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER,
                       GL_TEXTURE_MIN_FILTER, GL_TEXTURE_WRAP_R,
                       GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_UNSIGNED_BYTE,
                       glBindTexture, glGenTextures, glTexImage3D,
                       glTexParameteri, glTexSubImage3D)
from PIL import Image
from tqdm import tqdm


class TextureManager:
    """
    TextureManager

    A class to manage the textures used in the game
    """

    def __init__(self, n_textures):
        # Create a new texture object and bind it
        self.tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_3D, self.tex)

        # Set the texture parameters
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        self.width = 32
        self.height = 32
        self.depth = n_textures

        # Create the initial data for the texture
        self.data = np.zeros((self.width, self.height, self.depth, 4), dtype=np.uint8)

        # Use glTexImage3D to upload the data to the texture
        glTexImage3D(GL_TEXTURE_3D, 0, GL_RGBA8, self.width, self.height,
                     self.depth, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.data)

        # Set the current depth to 0
        self.current_depth = 0
        self.texture_coords = {}
        self._texture_coords = []

    def add_slice(self, filepath):
        """
        Add a slice to the texture

        :param filepath: The path to the image file to add

        :return: The texture coordinates for the added slice
        """
        # Load the image data from the file using PIL
        image = Image.open(filepath)
        image_data = np.array(image)

        # Convert the image data to the correct format and shape
        image_data = image_data[:, :, :3]  # Drop the alpha channel if present
        image_data = np.ascontiguousarray(
            image_data[:, :, ::-1])  # Convert from RGB to BGR
        # Add a singleton dimension for the z axis
        image_data = np.expand_dims(image_data, axis=2)

        # Update the texture using glTexSubImage3D
        glTexSubImage3D(GL_TEXTURE_3D, 0, 0, 0, self.current_depth,
                        image.size[0], image.size[1], 1, GL_BGR, GL_UNSIGNED_BYTE, image_data)

        # Increment the current depth
        self.current_depth += 1

        # Return the texture coordinates for the added slice
        x1, y1, x2, y2 = 0, 0, 1, 1
        z = self.current_depth / self.data.shape[2]
        self.texture_coords[filepath] = (
            x1, y1, z, x2, y1, z, x2, y2, z, x1, y2, z)
        self._texture_coords.append({
            "filepath": filepath,
            "coords": (x1, y1, z, x2, y1, z, x2, y2, z, x1, y2, z)
        })
        return self.texture_coords[filepath]

    def get_texture_coords(self, filepath):
        """
        Get the texture coordinates for a slice

        :param filepath: The path to the image file to get the texture coordinates for

        :return: The texture coordinates for the slice
        """
        return self.texture_coords[filepath]

    def bind(self):
        """
        Bind the texture
        """
        glBindTexture(GL_TEXTURE_3D, self.tex)

    def get_texcoords_from_index(self, index):
        return self._texture_coords[index]["coords"]

    def get_texture_index(self, filepath):
        for i, texture in enumerate(self._texture_coords):
            if texture["filepath"] == filepath:
                return i
        return -1
    
    def add_from_folder(self, folder):
        """
        Add all the slices in a folder to the texture

        :param folder: The folder to add the slices from
        """
        # Get all the files in the folder
        files = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]

        # Add each file to the texture
        for file in tqdm(files, desc=f"Loading textures from {folder}"):
            self.add_slice(file)
