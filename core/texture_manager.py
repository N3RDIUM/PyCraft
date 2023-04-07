# imports
from os import listdir
from os.path import basename, isfile, join

import numpy as np
from OpenGL.GL import *
from PIL import Image
from tqdm import tqdm

class TextureManager:
    """
    TextureManager

    A class to manage the textures used in the game
    """

    def __init__(self, max_textures=256):
        """
        Initialize the TextureManager
        Use a 3d texture array to store the textures

        :param n_textures: The number of textures to allocate
        """
        # Create the texture array
        self.texture_array = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture_array)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # Set the maximum number of textures
        self.n_textures = max_textures
        self.current_texture = 0

        # Create the texture list
        self.textures = {}
        
    def load_textures(self, texture_dir):
        """
        Load the textures from the given directory

        :param texture_dir: The directory to load the textures from
        """
        # Load the textures
        for texture_file in tqdm([join(texture_dir, f) for f in listdir(texture_dir) if isfile(join(texture_dir, f))]):
            self.load_texture(texture_file)
            
    def load_texture(self, texture_file):
        """
        Load the texture from the given file

        :param texture_file: The file to load the texture from
        """
        # Load the texture
        texture = Image.open(texture_file)
        texture = texture.convert("RGBA")
        texture = texture.transpose(Image.FLIP_TOP_BOTTOM)
        texture_data = np.array(list(texture.getdata()), np.uint8)
        
        # Generate the texture
        glTexImage3D(
            GL_TEXTURE_2D_ARRAY, 0,
            GL_RGBA8, texture.width, texture.height, self.n_textures,
            0, GL_RGBA, GL_UNSIGNED_BYTE, None
        )
        glTexSubImage3D(
            GL_TEXTURE_2D_ARRAY, 0, 0, 0, self.current_texture,
            texture.width, texture.height, 1,
            GL_RGBA, GL_UNSIGNED_BYTE, texture_data
        )
        
        # Add the texture to the list
        self.textures[basename(texture_file)] = self.current_texture
        self.current_texture += 1
        
    def get_texture(self, texture_name):
        """
        Get the texture with the given name

        :param texture_name: The name of the texture to get
        """
        return self.textures[texture_name]
    
    def get_texcoords(self, texture_name):
        """
        Get the texture coordinates for the given texture

        :param texture_name: The name of the texture to get the coordinates for
        """
        # Get the texture
        texture_idx = self.get_texture(texture_name)
        
        coords__3d = np.array([
            0.0, 0.0, texture_idx,
            1.0, 0.0, texture_idx,
            1.0, 1.0, texture_idx,
            0.0, 1.0, texture_idx
        ], np.float32)
        
        return coords__3d
    
    def bind(self):
        """
        Bind the texture array
        """
        glActiveTexture(GL_TEXTURE0)
        glGenerateMipmap(GL_TEXTURE_2D_ARRAY)
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture_array)