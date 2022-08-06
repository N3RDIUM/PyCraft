# imports
import glfw
from OpenGL.GL import *
from ctypes import *
from core.texture_manager import *
import threading
import numpy as np
from core.logger import *
from core.fileutils import *
from constants import *

glfw.init()

class TerrainRenderer:
    def __init__(self, window, mode=GL_QUADS):
        self.event = threading.Event()
        self._len  = 0
        self._len_ = 0

        self.parent = window
        self.mode = mode

        self.vertices  = []
        self.texCoords = []

        self.texture_manager = TextureAtlas()
        self.listener        = ListenerBase("cache_vbo/", window)
        self.writer          = WriterBase("cache_vbo/")

        self.create_vbo(window)

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

        while not glfw.window_should_close(window2):
            if self.listener.get_queue_length() > 0:
                try:
                    i = self.listener.get_queue_item(0)

                    vertices = np.array(i["vertices"], dtype=np.float32)
                    texture_coords = np.array(i["texCoords"], dtype=np.float32)

                    bytes_vertices = vertices.nbytes
                    bytes_texCoords = texture_coords.nbytes

                    verts = (GLfloat * len(vertices))(*vertices)
                    texCoords = (GLfloat * len(texture_coords))(*texture_coords)

                    log_vertex_addition((vertices, texture_coords), (bytes_vertices, bytes_texCoords), self._len*4, self._len_*4, self.listener.get_queue_length())

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

                    self.vertices += tuple(vertices)
                    self.texCoords += tuple(texture_coords)
                    
                    self._len += bytes_vertices
                    self._len_ += bytes_texCoords

                except Exception as e:
                    pass
                
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
        self.writer.write("AUTO", {
            "vertices": vertices,
            "texCoords": texCoords,
        })

    def remove(self, vertices, texCoords):
        raise NotImplementedError

    def add_mesh(self, storage):
        self.add(storage.vertices, storage.texCoords)

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

        glDrawArrays (self.mode, 0, self._len)

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)

class TerrainMeshStorage:
    def __init__(self, renderer):
        self.vertices = []
        self.texCoords = []
        self.renderer = renderer
        self.texture_manager = renderer.texture_manager
    
    def add(self, posList, texCoords):
        self.vertices.extend(posList)
        self.texCoords.extend(texCoords)
