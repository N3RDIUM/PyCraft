# imports
import ctypes

from OpenGL.GL import *

from core.buffer import Buffer
from settings import *

# constants
flags = GL_MAP_WRITE_BIT | GL_MAP_PERSISTENT_BIT | GL_MAP_COHERENT_BIT


class Renderer:
    """
    Renderer

    The renderer class for PyCraft: with buffer threading support.
    """

    def __init__(self, window, texture_manager):
        """
        Initializes the renderer.
        """
        # Window stuff
        self.window = window
        self.window.schedule_mainloop(self)

        # Texture stuff
        self.texture_manager = texture_manager
        
        # buffer stuff
        self.buffers = {}
        self.create_buffer("default")

        # OpenGL stuff
        self.sync = GLsync
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    def create_buffer(self, id):
        """
        Creates a buffer.

        :param id: The ID of the buffer.
        """
        # Create the buffers
        vertices_vbo = Buffer(id + "_vertices")
        texture_vbo = Buffer(id + "_texture")
        
        self.buffers[id] = {
            "vertices_buffer": vertices_vbo,
            "texture_buffer": texture_vbo,
            "vertices": [],
            "texture": [],
            "enabled": True,
        }

    def modify(self, id, vertices, texture, offset=0):
        """
        Modifies a buffer's data.

        :param id: The ID of the buffer.
        :param vertices: The vertices.
        :param texture: The texture.
        :param offset: The offset.
        """
        # Modify the buffers
        self.buffers[id]["vertices_buffer"].modify(vertices, offset)
        self.buffers[id]["texture_buffer"].modify(texture, offset)
        self.buffers[id]["vertices"][offset:offset + len(vertices)] = vertices
        self.buffers[id]["texture"][offset:offset + len(texture)] = texture

    def drawcall(self):
        """
        Renders the buffers.
        """
        # Texture stuff
        glEnable(GL_TEXTURE_3D)
        self.texture_manager.bind()

        for id in self.buffers.keys():
            buffer = self.buffers[id]
            if buffer["enabled"]: # If the buffer is enabled
                glBindBuffer(GL_ARRAY_BUFFER, buffer["vertices_buffer"].buf)
                glVertexPointer(3, GL_FLOAT, 8 * 4, None)
                glBindBuffer(GL_ARRAY_BUFFER, buffer["texture_buffer"].buf)
                glTexCoordPointer(2, GL_FLOAT, 8 * 4, None)
                glDrawArrays(GL_TRIANGLES, 0, len(buffer["vertices"]))

        # Texture stuff
        glDisable(GL_TEXTURE_3D)
