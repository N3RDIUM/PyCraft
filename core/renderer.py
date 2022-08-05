# imports
import glfw
from OpenGL.GL import *
from ctypes import *
from core.texture_manager import *
import threading
import numpy as np
from core.logger import *
from constants import *

glfw.init()

class TerrainRenderer:
    def __init__(self, window):
        self.event = threading.Event()
        self.to_add = []
        self._len  = 0
        self._len_ = 0

        self.parent = window

        self.vertices = []
        self.texCoords = []

        self.create_vbo(window)

        self.texture_manager = TextureAtlas()

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if not USING_RENDERDOC:
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    def shared_context(self, window):
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window2 = glfw.create_window(500,500, "Window 2", None, window)
        glfw.make_context_current(window2)
        self.event.set()

        while not glfw.window_should_close(window):
            if len(self.to_add) > 0:
                i = self.to_add.pop(0)

                vertices = np.array(i[0], dtype=np.float32)
                texture_coords = np.array(i[1], dtype=np.float32)

                bytes_vertices = vertices.nbytes
                bytes_texCoords = texture_coords.nbytes

                verts = (GLfloat * len(vertices))(*vertices)
                texCoords = (GLfloat * len(texture_coords))(*texture_coords)

                log_vertex_addition((vertices, texture_coords), (bytes_vertices, bytes_texCoords), self._len*4, len(self.to_add))

                glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
                glBufferSubData(GL_ARRAY_BUFFER, self._len, bytes_vertices, verts)
                if not USING_RENDERDOC:
                    glVertexPointer (3, GL_FLOAT, 0, None)
                glFlush()
                
                glBindBuffer(GL_ARRAY_BUFFER, self.vbo_1)
                glBufferSubData(GL_ARRAY_BUFFER, self._len_, bytes_texCoords, texCoords)
                if not USING_RENDERDOC:
                    glTexCoordPointer(2, GL_FLOAT, 0, None)
                glFlush()

                self.vertices += i[0]
                self.texCoords += i[1]
                
                self._len += bytes_vertices
                self._len_ += bytes_texCoords

            glfw.poll_events()
            glfw.swap_buffers(window2)
        glfw.terminate()

    def create_vbo(self, window):
        self.vbo, self.vbo_1 = glGenBuffers (2)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, 64000000, None, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_1)
        glBufferData(GL_ARRAY_BUFFER, 64000000, None, GL_STATIC_DRAW)

        glfw.make_context_current(None)
        thread = threading.Thread(target=self.shared_context, args=[window], daemon=True)
        thread.start()
        self.event.wait()
        glfw.make_context_current(window)

    def add(self, vertices, texCoords):
        self.to_add.append((tuple(vertices), tuple(texCoords)))

    def render(self):
        glClear (GL_COLOR_BUFFER_BIT)

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBindBuffer (GL_ARRAY_BUFFER, self.vbo)
        if not USING_RENDERDOC:
            glVertexPointer (3, GL_FLOAT, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_1)
        if not USING_RENDERDOC:
            glTexCoordPointer(2, GL_FLOAT, 0, None)

        glDrawArrays (GL_QUADS, 0, self._len)

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)