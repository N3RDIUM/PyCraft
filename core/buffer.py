# imports
import ctypes
import random

import numpy as np
from OpenGL.GL import *

from settings import INIT_VBO_SIZE


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
        self.size = INIT_VBO_SIZE
        glBindBuffer(GL_ARRAY_BUFFER, self.buf)

        # Allocate storage for the buffer using glBufferStorage and specify the desired storage flags
        glBufferStorage(GL_ARRAY_BUFFER, self.size, None,
                        GL_MAP_WRITE_BIT | GL_MAP_PERSISTENT_BIT)

    def map_buffer(self):
        """
        Maps the buffer to memory.
        """
        # Bind the buffer
        glBindBuffer(GL_ARRAY_BUFFER, self.buf)

        # Map the buffer to memory using glMapBufferRange
        ptr = glMapBufferRange(GL_ARRAY_BUFFER, 0, self.size,
                               GL_MAP_WRITE_BIT | GL_MAP_PERSISTENT_BIT)

        # Create a pointer to the data buffer object
        self.data_ptr = ctypes.cast(ptr, ctypes.POINTER(GLfloat * self.size))

    def unmap_buffer(self):
        """
        Unmaps the buffer.
        """
        # Unmap the buffer
        glUnmapBuffer(GL_ARRAY_BUFFER)

        # Unbind the buffer
        glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    def extend_vbo(self, new_size):
        self.map_buffer()
        data = np.asarray(self.data_ptr.contents)
        glFlush()
        self.unmap_buffer()
        self.size = new_size
        glDeleteBuffers(1, [self.buf])
        self.buf = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.buf)
        # Allocate storage for the buffer using glBufferData and specify the desired storage flags
        glBufferStorage(GL_ARRAY_BUFFER, self.size, None,
                        GL_MAP_WRITE_BIT | GL_MAP_PERSISTENT_BIT)
        self.map_buffer()
        new_data = np.empty(new_size, dtype=data.dtype)
        new_data[:len(data)] = data
        self.data_ptr.contents = new_data.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p))
        glFlush()
        self.unmap_buffer()
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glFlush()
        
    def print_buffer_size(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.buf)
        print("Buffer size: %d bytes" % glGetBufferParameteriv(GL_ARRAY_BUFFER, GL_BUFFER_SIZE))

    def modify(self, data, offset=0):
        """
        Adds data to the buffer.

        :param data: The data to add to the buffer.
        :param offset: The offset to start writing at.
        """
        # Modify the buffer
        if offset+len(data) > self.size:
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            self.extend_vbo(offset+len(data))
            glFlush()
        # Print the size of the buffer for debugging
        # self.print_buffer_size()
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