# imports
import glfw
from OpenGL.GL import *
from ctypes import *
from core.texture_manager import *

glfw.init()

class VBOManager:
    def __init__(self, renderer):
        self.renderer = renderer
        self.run()
    
    def run(self):
        for i in self.renderer.to_add[:self.renderer.to_add_count]:
            vertices = i[0]
            texCoords = i[1]

            try:
                # use glBufferSubData
                glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo)
                glBufferSubData(GL_ARRAY_BUFFER, len(self.renderer.vertices)*4, len(vertices)*4, (c_float * len(vertices))(*vertices))
                glFlush()
                glVertexPointer(3, GL_FLOAT, 0, None)
                glTexCoordPointer(3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_1)
                glBufferSubData(GL_ARRAY_BUFFER, len(self.renderer.texCoords)*4, len(texCoords)*4, (c_float * len(texCoords))(*texCoords))
                glFlush()

                self.renderer.vertices.extend(i[0])
                self.renderer.texCoords.extend(i[1])
            except:
                print("Error")

            self.renderer.to_add.remove(i)

class TerrainRenderer:
    def __init__(self, window):
        self.window = window

        self.vertices = []
        self.texCoords = []

        self.to_add = []
        self.to_add_count = 256

        self.vbo, self.vbo_1 = glGenBuffers (2)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, 640000000, None, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_1)
        glBufferData(GL_ARRAY_BUFFER, 640000000, None, GL_STATIC_DRAW)
        self.vbo_manager = VBOManager(self)

        self.texture_manager = TextureAtlas()

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState (GL_VERTEX_ARRAY)

    def render(self):
        self.to_add_count = round(len(self.to_add) / 32)
        self.vbo_manager.run()

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

    def add(self, posList, texCoords):
        self.to_add.append((posList, texCoords))