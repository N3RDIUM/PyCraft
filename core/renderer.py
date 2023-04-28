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
        
        # Texture stuff
        self.texture_manager = texture_manager
        
        # buffer stuff
        self.buffers = {}
        self.create_buffer("default")

        # OpenGL stuff
        self.sync = GLsync
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnable(GL_TEXTURE_2D)

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
        if offset == -1:
            offset = len(self.buffers[id]["vertices"])
        # Modify the buffers
        self.buffers[id]["vertices_buffer"].modify(vertices, offset)
        self.buffers[id]["texture_buffer"].modify(texture, offset)
        self.buffers[id]["vertices"][offset:offset + len(vertices)] = vertices
        self.buffers[id]["texture"][offset:offset + len(texture)] = texture

    def drawcall(self):
        """
        Renders the buffers.
        """
        for id in self.buffers.keys():
            buffer = self.buffers[id]
            if buffer["enabled"]: # If the buffer is enabled
                buffer["vertices_buffer"].bind()
                glVertexPointer(3, GL_FLOAT, 0, None)
                buffer["texture_buffer"].bind()
                glTexCoordPointer(2, GL_FLOAT, 0, None)
                glDrawArrays(GL_TRIANGLES, 0, len(buffer["vertices"]) // 3)
                glBindBuffer(GL_ARRAY_BUFFER, 0)