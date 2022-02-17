# imports
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from ctypes import c_float

glfw.init()

class TerrainRenderer:
    def __init__(self, window):
        self.window = window

        self.vertices = []

        self.vbo = glGenBuffers (1)
        glBindBuffer (GL_ARRAY_BUFFER, self.vbo)

    def render(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glVertexPointer (3, GL_FLOAT, 0, None)
        glDrawArrays(GL_QUADS, 0, len(self.vertices))

    def add_cube(self, pos):
        x, y, z = pos
        X, Y, Z = x + 1, y + 1, z + 1

        # add a quad
        self.vertices.extend([
            # top
            x, y, z,
            x, y, Z,
            X, y, Z,
            X, y, z,

            # bottom
            x, Y, z,
            X, Y, z,
            X, Y, Z,
            x, Y, Z,

            # left
            x, y, z,
            x, Y, z,
            x, Y, Z,
            x, y, Z,

            # right
            X, y, z,
            X, y, Z,
            X, Y, Z,
            X, Y, z,

            # front
            x, y, z,
            x, Y, z,
            X, Y, z,
            X, y, z,

            # back
            x, y, Z,
            X, y, Z,
            X, Y, Z,
            x, Y, Z,
        ])

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(self.vertices) * 4, (c_float * len(self.vertices))(*self.vertices), GL_STATIC_DRAW)
        glFlush()

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, None)
