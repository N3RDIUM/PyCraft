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
import time

glfw.init()

VERTICES_SIZE = 256 * 16 * 16 * 8 * 24 * 3
TEXCOORDS_SIZE = 256 * 16 * 16 * 8 * 24 * 2

class TerrainRenderer:
    def __init__(self, window, mode=GL_TRIANGLES):
        self.event = threading.Event()

        self.parent = window
        self.mode = mode
        self.vbos = {}

        self.texture_manager = TextureAtlas()
        self.listener        = ListenerBase("cache/vbo/")
        self.writer          = WriterBase("cache/vbo/")

        self.init(window)

        self.create_vbo("DEFAULT")

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        if not USING_RENDERDOC:
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    
    def create_vbo(self, id):
        self.vbo, self.vbo_1 = glGenBuffers (2)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, VERTICES_SIZE, None, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_1)
        glBufferData(GL_ARRAY_BUFFER, TEXCOORDS_SIZE, None, GL_DYNAMIC_DRAW)
        self.vbos[id] = {
            "vbo": self.vbo,
            "vbo_1": self.vbo_1,
            "_len": 0,
            "_len_": 0,
            "vertices": (),
            "texCoords": (),
            "render": True,
            "addition_history": []
        }

    def shared_context(self, window):
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window2 = glfw.create_window(500,500, "Window 2", None, window)
        glfw.make_context_current(window2)
        self.event.set()

        while not glfw.window_should_close(window):
            try:
                time.sleep(0.04)
                if self.listener.get_queue_length() > 0:
                    i = self.listener.get_random_item()[0]
                    id = i["id"]
                    data = self.vbos[id]
                    vbo = data["vbo"]
                    vbo_1 = data["vbo_1"]
                    _vertices = data["vertices"]
                    _texCoords = data["texCoords"]
                    _len = data["_len"]
                    _len_ = data["_len_"]
                    
                    vertices = np.array(i["vertices"], dtype=np.float32)
                    texture_coords = np.array(i["texCoords"], dtype=np.float32)

                    bytes_vertices = vertices.nbytes
                    bytes_texCoords = texture_coords.nbytes

                    verts = (GLfloat * len(vertices))(*vertices)
                    texCoords = (GLfloat * len(texture_coords))(*texture_coords)

                    # Check if the data is already in the VBO
                    if verts in data["addition_history"]:
                        continue
                    if texCoords in data["addition_history"]:
                        continue                    

                    log_vertex_addition((vertices, texture_coords), (bytes_vertices, bytes_texCoords), _len*4, _len_*4, self.listener.get_queue_length())

                    glBindBuffer(GL_ARRAY_BUFFER, vbo)
                    glBufferSubData(GL_ARRAY_BUFFER, _len, bytes_vertices, verts)
                    if not USING_RENDERDOC:
                        glVertexPointer (3, GL_FLOAT, 0, None)
                    glFlush()
                    
                    glBindBuffer(GL_ARRAY_BUFFER, vbo_1)
                    glBufferSubData(GL_ARRAY_BUFFER, _len_, bytes_texCoords, texCoords)
                    if not USING_RENDERDOC:
                        glTexCoordPointer(2, GL_FLOAT, 0, None)
                    glFlush()

                    _vertices += tuple(vertices)
                    _texCoords += tuple(texture_coords)
                    
                    _len += bytes_vertices
                    _len_ += bytes_texCoords

                    data["_len"] = _len
                    data["_len_"] = _len_
                    data["vertices"] = _vertices
                    data["texCoords"] = _texCoords
                    data["addition_history"].append((vertices, texture_coords))
            except:
                pass
            glfw.swap_buffers(window2)
        glfw.terminate()
        self.event.set()
        self.listener.thread.join()
        del self.listener

    def init(self, window):
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
        to_add = storage._group()

        for i in to_add:
            self.add(i[0], i[1])

    def render(self):
        glClear (GL_COLOR_BUFFER_BIT)

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        for data in self.vbos.values():
            if data["render"]:
                glBindBuffer(GL_ARRAY_BUFFER, data["vbo"])
                if not USING_RENDERDOC:
                    glVertexPointer (3, GL_FLOAT, 0, None)
                glFlush()
                
                glBindBuffer(GL_ARRAY_BUFFER, data["vbo_1"])
                if not USING_RENDERDOC:
                    glTexCoordPointer(2, GL_FLOAT, 0, None)
                glFlush()

                glDrawArrays(self.mode, 0, data["_len"] * 4)

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)