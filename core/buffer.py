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
        glBufferStorage(GL_ARRAY_BUFFER, INIT_VBO_SIZE, None,
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
        
    def grow_buffer(self, size):
        glBindBuffer(GL_COPY_READ_BUFFER, self.buf)
        newbuf = glGenBuffers(1)
        glBindBuffer(GL_COPY_WRITE_BUFFER, newbuf)
        glBufferData(GL_COPY_WRITE_BUFFER, size, None, GL_STATIC_DRAW)
        glCopyBufferSubData(GL_COPY_READ_BUFFER, GL_COPY_WRITE_BUFFER, 0, 0, self.size)
        # Now we have a new buffer with the same data, so we can delete the old one and create a new one with the persistent mapping
        glDeleteBuffers(1, [self.buf])
        self.buf = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.buf)
        self.size = size
        # Allocate storage for the buffer using glBufferStorage and specify the desired storage flags
        glBufferStorage(GL_ARRAY_BUFFER, self.size, None,
                        GL_MAP_WRITE_BIT | GL_MAP_PERSISTENT_BIT)
        # Now copy the data from the new buffer to the old one
        glBindBuffer(GL_COPY_READ_BUFFER, newbuf)
        glBindBuffer(GL_COPY_WRITE_BUFFER, self.buf)
        glCopyBufferSubData(GL_COPY_READ_BUFFER, GL_COPY_WRITE_BUFFER, 0, 0, self.size)
        glBufferData(GL_COPY_READ_BUFFER, 0, None, GL_STATIC_DRAW)
        glDeleteBuffers(1, [newbuf]) # Delete the new buffer
    
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
            self.grow_buffer(offset+len(data))
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