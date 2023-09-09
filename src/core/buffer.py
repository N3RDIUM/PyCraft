# imports
import ctypes
import random

import numpy as np
from OpenGL.GL import *

# TODO: Make this configurable
VBO_SIZE = 1000000


class Buffer:
    """
    Buffer

    This is a wrapper for OpenGL buffer objects.
    It supports persistent mapping.
    """

    def __init__(self, id):
        """
        Initializes the buffer.
        """
        self.id = id
        self.buf = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.buf)

        # Allocate storage for the buffer using glBufferStorage and specify the desired storage flags
        glBufferStorage(GL_ARRAY_BUFFER, VBO_SIZE, None,
                        GL_MAP_WRITE_BIT | GL_MAP_PERSISTENT_BIT)

    def map_buffer(self):
        """
        Maps the buffer to memory.
        """
        # Bind the buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.buf)

        # Map the buffer to memory using glMapBufferRange
        ptr = glMapBufferRange(GL_ARRAY_BUFFER, 0, VBO_SIZE,
                               GL_MAP_WRITE_BIT | GL_MAP_PERSISTENT_BIT)

        # Create a pointer to the data buffer object
        self.data_ptr = ctypes.cast(ptr, ctypes.POINTER(GLfloat * VBO_SIZE))

    def unmap_buffer(self):
        """
        Unmaps the buffer.
        """
        # Unmap the buffer
        glUnmapBuffer(GL_ARRAY_BUFFER)

        # Unbind the buffer
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def modify(self, data, offset=0):
        """
        Adds data to the buffer.

        :param data: The data to add to the buffer.
        :param offset: The offset to start writing at.
        """
        # Modify the buffer
        self.map_buffer()
        self.data_ptr.contents[offset:offset + len(data)] = data
        glFlush()
        self.unmap_buffer()
    
    def bind(self):
        """
        Binds the buffer.
        """
        glBindBuffer(GL_ARRAY_BUFFER, self.buf)
        
    def __del__(self):
        """
        Deletes the buffer.
        """
        glDeleteBuffers(1, [self.buf])