# imports
import ctypes

import pyglet
from OpenGL.GL import (GL_NEAREST, GL_RGBA, GL_TEXTURE_2D_ARRAY,
                       GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER,
                       GL_UNSIGNED_BYTE, GLuint, glBindTexture,
                       glGenerateMipmap, glGenTextures, glTexImage3D,
                       glTexParameteri, glTexSubImage3D)

########################################################################
# Implementation from https://github.com/obiwac/python-minecraft-clone #
########################################################################


class TextureManager:
    """
    TextureManager

    A texture manager for PyCraft.
    """

    def __init__(self, texture_width=32, texture_height=32, max_textures=1024):
        self.texture_width = texture_width
        self.texture_height = texture_height

        self.max_textures = max_textures

        self.textures = []
        self.texture_indexes = {}

        self.texture_array = GLuint(0)
        glGenTextures(1, self.texture_array)
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture_array)

        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D_ARRAY, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glTexImage3D(
            GL_TEXTURE_2D_ARRAY, 0, GL_RGBA,
            self.texture_width, self.texture_height, self.max_textures,
            0, GL_RGBA, GL_UNSIGNED_BYTE, None)

    def generate_mipmaps(self):
        glGenerateMipmap(GL_TEXTURE_2D_ARRAY)

    def add_texture(self, texture):
        if not texture in self.textures:
            self.textures.append(texture)

            texture_image = pyglet.image.load(
                f"textures/{texture}.png").get_image_data()
            glBindTexture(GL_TEXTURE_2D_ARRAY, self.texture_array)

            glTexSubImage3D(
                GL_TEXTURE_2D_ARRAY, 0,
                0, 0, self.textures.index(texture),
                self.texture_width, self.texture_height, 1,
                GL_RGBA, GL_UNSIGNED_BYTE,
                texture_image.get_data("RGBA", texture_image.width * 4))

            self.texture_indexes[texture] = self.textures.index(texture)

    def get_texture_index(self, texture):
        return self.texture_indexes[texture]

    def generate_texture_coords(self, texture):
        return [
            0, self.get_texture_index(texture), 0,
            1, self.get_texture_index(texture), 0,
            1, self.get_texture_index(texture), 1,
            0, self.get_texture_index(texture), 1
        ]
