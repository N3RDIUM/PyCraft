# imports
from os import listdir
from os.path import basename, exists, isfile, join

import numpy as np
from OpenGL.GL import (GL_BGR, GL_NEAREST, GL_REPEAT, GL_RGBA, GL_RGBA8,
                       GL_TEXTURE0, GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER,
                       GL_TEXTURE_MIN_FILTER, GL_TEXTURE_WRAP_R,
                       GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_UNSIGNED_BYTE,
                       glActiveTexture, glBindTexture, glEnable,
                       glGenerateMipmap, glGenTextures, glTexImage3D,
                       glTexParameteri, glTexSubImage3D)
from PIL import Image
from tqdm import tqdm


# imports
from os import listdir
from os.path import basename, exists, isfile, join

import numpy as np
from OpenGL.GL import (GL_TEXTURE_2D_ARRAY, GL_NEAREST, GL_REPEAT, GL_RGBA,
                       GL_TEXTURE0, GL_TEXTURE_MAG_FILTER,
                       GL_TEXTURE_MIN_FILTER, GL_TEXTURE_WRAP_R,
                       GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_UNSIGNED_BYTE,
                       glActiveTexture, glBindTexture, GL_TEXTURE_MAX_LEVEL, GL_TEXTURE_BASE_LEVEL,
                       glGenTextures, glTexImage3D,
                       glTexParameteri, glTexSubImage3D, GLuint)
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

        :param n_textures: The number of textures to allocate
        """
        self.texture_width = 32
        self.texture_height = 32

        self.max_textures = max_textures

        self.textures = []
        self.texture_coords = {}

        self.texture_array = GLuint(0)
        glGenTextures(1, self.texture_array)
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture_array)

        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_WRAP_R, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTexImage3D(
            GL_TEXTURE_2D_ARRAY, 0, GL_RGBA,
            self.texture_width, self.texture_height, self.max_textures,
            0, GL_RGBA, GL_UNSIGNED_BYTE, None)

        # Set mipmap range parameters
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_BASE_LEVEL, 0)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAX_LEVEL, 0)

    def add_texture(self, texture):
        if not texture in self.textures:
            _texture_name = basename(texture)
            self.textures.append(_texture_name)
            z = self.textures.index(_texture_name)
            self.texture_coords[_texture_name] = (
                0, 0, z,
                1, 0, z,
                1, 1, z,
                1, 1, z,
                1, 0, z,
                0, 1, z
            )

            texture_image = Image.open(texture)
            texture_data = np.array(list(texture_image.getdata()), np.uint8)

            glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture_array)
            glTexSubImage3D(
                GL_TEXTURE_2D_ARRAY, 0,
                0, 0, self.textures.index(_texture_name),
                self.texture_width, self.texture_height, 1 / self.max_textures,
                GL_RGBA, GL_UNSIGNED_BYTE,
                texture_data)
            glGenerateMipmap(GL_TEXTURE_2D_ARRAY)
            glBindTexture(GL_TEXTURE_2D_ARRAY, 0)

    def get_texture_coords(self, filepath):
        """
        Get the texture coordinates for a slice

        :param filepath: The path to the image file to get the texture coordinates for

        :return: The texture coordinates for the slice
        """
        return self.texture_coords[filepath]

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
        files = [join(folder, f)
                 for f in listdir(folder) if isfile(join(folder, f))]

        # Add each file to the texture
        for file in tqdm(files, desc=f"Loading textures from {folder}"):
            self.add_texture(file)

    def bind(self):
        """
        Generate mipmaps and bind the texture
        """
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture_array)
