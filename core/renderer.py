# imports
import glfw
from OpenGL.GL import *
from ctypes import *
from core.texture_manager import *
import threading

glfw.init()

class TerrainRenderer:
    def __init__(self, window):
        self.event = threading.Event()
        self.to_add = []
        self._len = 0

        self.parent = window

        self.vertices = []
        self.texCoords = []

        self.texture_manager = TextureAtlas()

        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState (GL_VERTEX_ARRAY)

        self.create_vbo(window)

    def shared_context(self, window):
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window2 = glfw.create_window(500,500, "Window 2", None, window)
        glfw.make_context_current(window2)
        self.event.set()

        while not glfw.window_should_close(window):
            if len(self.to_add) > 0:
                i = self.to_add.pop(0)

                glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
                glBufferSubData(GL_ARRAY_BUFFER, self._len, len(i[0])*4, (GLfloat * len(i[0]))(*i[0]))
                glBindBuffer(GL_ARRAY_BUFFER, self.vbo_1)
                glBufferSubData(GL_ARRAY_BUFFER, self._len, len(i[1])*4, (GLfloat * len(i[1]))(*i[1]))
                glFlush()

                self.vertices += i[0]
                self.texCoords += i[1]
                
                self._len += len(i[0])*4

            glfw.poll_events()
            glfw.swap_buffers(window2)
        glfw.terminate()

    def create_vbo(self, window):
        self.vbo, self.vbo_1 = glGenBuffers (2)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, 640000, None, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_1)
        glBufferData(GL_ARRAY_BUFFER, 640000, None, GL_STATIC_DRAW)
        glfw.make_context_current(None)
        thread = threading.Thread(target=self.shared_context, args=[window], daemon=True)
        thread.start()
        self.event.wait()
        glfw.make_context_current(window)

        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState (GL_VERTEX_ARRAY)

    def add(self, vertices, texCoords):
        self.to_add.append((tuple(vertices), tuple(texCoords)))

    def render(self):
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
