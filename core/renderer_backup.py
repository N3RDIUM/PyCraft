# imports
import glfw, numpy as np
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
            print(i)
            vertices = np.array(i[0], dtype=np.float32)
            texCoords = np.array(i[1], dtype=np.float32)

            # use glBufferSubData
            glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo)
            glBufferData(GL_ARRAY_BUFFER, self.renderer.vertices.nbytes, vertices.nbytes, (c_float * len(vertices))(*vertices))
            glFlush()
            glVertexPointer(3, GL_FLOAT, 0, None)
            glTexCoordPointer(3, GL_FLOAT, 0, None)
            glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_1)
            glBufferSubData(GL_ARRAY_BUFFER, self.renderer.texCoords.nbytes, texCoords.nbytes, (c_float * len(texCoords))(*texCoords))
            glFlush()

            self.renderer.vertices.extend(i[0])
            self.renderer.texCoords.extend(i[1])

            self.renderer.to_add.remove(i)

class TerrainRenderer:
    def __init__(self, window):
        self.window = window

        self.vertices = np.array([])
        self.texCoords = np.array([])

        self.to_add = []
        self.to_add_count = 256

        self.vbo, self.vbo_1 = glGenBuffers (2)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, 8*16*256*4, None, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_1)
        glBufferData(GL_ARRAY_BUFFER, 8*16*256*4, None, GL_STATIC_DRAW)
        self.vbo_manager = VBOManager(self)

        self.texture_manager = TextureAtlas()

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState (GL_VERTEX_ARRAY)

    def render(self):
        try:
            self.vbo_manager.run()
        except RuntimeError:
            pass

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
        self.to_add.append((np.array(posList), np.array(texCoords)))
        print(self.to_add[-1])

    def update_vbo(self):
        pass