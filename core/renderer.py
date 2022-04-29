# imports
import glfw, numpy
from OpenGL.GL import *
from ctypes import *
from core.texture_manager import *
import threading
from pprint import pprint

glfw.init()
event = threading.Event()

class VBOManager:
    def __init__(self, renderer):
        self.renderer = renderer
        glfw.make_context_current(None)
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
        event.wait()
        glfw.make_context_current(self.renderer.window)
    
    def run(self):
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        self.window = glfw.create_window(300, 300, "Window 2", None, self.renderer.window)
        glfw.make_context_current(self.window)
        event.set()

        while not glfw.window_should_close(self.renderer.window):
            while self.renderer.rendering:
                pass
            self.renderer.allow_rendering = False

            for i in range(0,self.renderer.to_add_count):
                if not len(self.renderer.to_add) == 0:
                    try:
                        self.renderer.vertices.extend(self.renderer.to_add[0][0])
                        self.renderer.texCoords.extend(self.renderer.to_add[0][1])
                        self.renderer.vertices_added = len(self.renderer.vertices)

                        self.renderer.to_add.remove(self.renderer.to_add[0])
                    except IndexError:
                        pass

            glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo)
            glBufferData(GL_ARRAY_BUFFER, len(self.renderer.vertices) * 4, (c_float * len(self.renderer.vertices))(*self.renderer.vertices), GL_STATIC_DRAW)
            glFlush()
            glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_1)
            glBufferData(GL_ARRAY_BUFFER, len(self.renderer.texCoords) * 4, (c_float * len(self.renderer.texCoords))(*self.renderer.texCoords), GL_STATIC_DRAW)
            glFlush()

            glfw.poll_events()
            glfw.swap_buffers(self.window)      

            self.renderer.allow_rendering = True  

class TerrainRenderer:
    def __init__(self, window):
        self.window = window

        self.vertices = []
        self.texCoords = []

        self.to_add = []
        self.to_add_count = 1024 * 1024

        self.vertices_added = 0

        self.rendering = False
        self.allow_rendering = True

        self.vbo, self.vbo_1 = glGenBuffers (2)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, 12 * 4, (c_float * 12)(0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_1)
        glBufferData(GL_ARRAY_BUFFER, 12 * 4, None, GL_DYNAMIC_DRAW)

        self.vbo_manager = VBOManager(self)

        self.texture_manager = TextureAtlas()

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState (GL_VERTEX_ARRAY)

    def render(self):
        if self.allow_rendering:
            self.rendering = True
            self.vbo_manager.run()

            glClear (GL_COLOR_BUFFER_BIT)

            glEnable(GL_TEXTURE_2D)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glBindBuffer (GL_ARRAY_BUFFER, self.vbo)
            glVertexPointer (3, GL_FLOAT, 0, None)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo_1)
            glTexCoordPointer(2, GL_FLOAT, 0, None)

            glDrawArrays (GL_QUADS, 0, len(self.vertices) * 4)
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_BLEND)

            self.rendering = False

    def add(self, posList, texCoords):
        self.to_add.append((numpy.array(posList), numpy.array(texCoords)))
        return len(self.to_add) - 1

    def make_urgent_update(self, index):
        i = index
        self.renderer.vertices.extend(i[0])
        self.renderer.texCoords.extend(i[1])
        self.renderer.to_add.remove(i)

        glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(self.renderer.vertices) * 4, (c_float * len(self.renderer.vertices))(*self.renderer.vertices), GL_STATIC_DRAW)
        glFlush()
        glBindBuffer(GL_ARRAY_BUFFER, self.renderer.vbo_1)
        glBufferData(GL_ARRAY_BUFFER, len(self.renderer.texCoords) * 4, (c_float * len(self.renderer.texCoords))(*self.renderer.texCoords), GL_STATIC_DRAW)
        glFlush()

    def update_vbo(self):
        pass
