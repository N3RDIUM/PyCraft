# imports
import glfw
import pygame
from OpenGL.GL import *
from ctypes import *
import threading, time

event = threading.Event()

glfw.init()

def loadTexture(path):
    texSurface = pygame.image.load(path)
    texData = pygame.image.tostring(texSurface, "RGBA", 1)
    width = texSurface.get_width()
    height = texSurface.get_height()
    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 
            0, GL_RGBA, GL_UNSIGNED_BYTE, texData)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    return texid

class TerrainRenderer:
    def __init__(self, window):
        self.window = window

        self.vertices = []
        self.texCoords = []

        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        self.vbo, self.vbo_1 = glGenBuffers (2)

        self.texture = loadTexture("assets/textures/block/bricks.png",)

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState (GL_VERTEX_ARRAY)


    def render(self):
        glClear (GL_COLOR_BUFFER_BIT)

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindBuffer (GL_ARRAY_BUFFER, self.vbo)
        glVertexPointer (3, GL_FLOAT, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_1)
        glTexCoordPointer(2, GL_FLOAT, 0, None)

        glDrawArrays (GL_QUADS, 0, len(self.vertices))
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)

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

        self.texCoords.extend([
            # top
            0, 0,
            0, 1,
            1, 1,
            1, 0,

            # bottom
            0, 0,
            1, 0,
            1, 1,
            0, 1,

            # left
            0, 0,
            0, 1,
            1, 1,
            1, 0,

            # right
            0, 0,
            1, 0,
            1, 1,
            0, 1,

            # front
            0, 0,
            0, 1,
            1, 1,
            1, 0,

            # back
            0, 0,
            1, 0,
            1, 1,
            0, 1,
        ])

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(self.vertices) * 4, (c_float * len(self.vertices))(*self.vertices), GL_STATIC_DRAW)
        glFlush()

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, None)

        glTexCoordPointer(3, GL_FLOAT, 0, None)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_1)
        glBufferData(GL_ARRAY_BUFFER, len(self.texCoords) * 4, (c_float * len(self.texCoords))(*self.texCoords), GL_STATIC_DRAW)
        glFlush()
