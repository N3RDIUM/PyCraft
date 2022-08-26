# imports
import glfw
import random
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

STEP = 1024
VERTICES_SIZE = 3200000
TEXCOORDS_SIZE = 3200000

class TerrainRenderer:
    def __init__(self, window, mode=GL_TRIANGLES):
        self.event = threading.Event()
        self.parent = window
        self.mode = mode
        self.vbos = {}
        self.texture_manager = TextureAtlas()
        
        self.listener        = ListenerBase("cache/vbo/")
        self.writer          = WriterBase("cache/vbo/")

        self.fps = 0
        self.timings = []

        self.initialise(window)

        glEnable(GL_TEXTURE_2D)
        if not USING_RENDERDOC:
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    def create_vbo(self, id):
        vbo, vbo_1 = glGenBuffers (2)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, VERTICES_SIZE, None, GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_1)
        glBufferData(GL_ARRAY_BUFFER, TEXCOORDS_SIZE, None, GL_STATIC_DRAW)

        self.vbos[id] = {
            "vbo_vertex": vbo,
            "vbo_texture": vbo_1,
            "vertices": (),
            "texCoords": (),
            "render": True
        }

        return id

    def delete_vbo(self, id):
        vbo = self.vbos[id]
        try:
            glDeleteBuffers(GL_ARRAY_BUFFER, pointer(vbo["vbo_vertex"]))
            glDeleteBuffers(GL_ARRAY_BUFFER, pointer(vbo["vbo_texture"]))
        except:
            pass
        del self.vbos[id]

    def initialise(self, window):
        glfw.make_context_current(None)
        thread = threading.Thread(target=self.shared_context, args=[window], daemon=True)
        thread.start()
        self.event.wait()
        glfw.make_context_current(window)

    def shared_context(self, window):
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        window2 = glfw.create_window(500,500, "Window 2", None, window)
        glfw.make_context_current(window2)
        self.event.set()

        while not glfw.window_should_close(window2):
            try:
                while self.listener.get_queue_length() == 0:
                    pass
                time.sleep(0.1)
                data = self.listener.get_first_item()
                id   = data["id"]

                vertices = np.array(data["vertices"], dtype=np.float32)
                texture_coords = np.array(data["texCoords"], dtype=np.float32)

                bytes_vertices = vertices.nbytes
                bytes_texCoords = texture_coords.nbytes

                verts = (GLfloat * len(vertices))(*vertices)
                texCoords = (GLfloat * len(texture_coords))(*texture_coords)

                vbo_dict = self.vbos[id]
                vbo = vbo_dict["vbo_vertex"]
                vbo_1 = vbo_dict["vbo_texture"]

                glBindBuffer(GL_ARRAY_BUFFER, vbo)
                glBufferSubData(GL_ARRAY_BUFFER, len(vbo_dict["vertices"])*4, bytes_vertices, verts)
                if not USING_RENDERDOC:
                    glVertexPointer (3, GL_FLOAT, 0, None)
                glFlush()
                
                glBindBuffer(GL_ARRAY_BUFFER, vbo_1)
                glBufferSubData(GL_ARRAY_BUFFER, len(vbo_dict["texCoords"])*4, bytes_texCoords, texCoords)
                if not USING_RENDERDOC:
                    glTexCoordPointer(2, GL_FLOAT, 0, None)
                glFlush()

                vbo_dict["vertices"] += tuple(vertices)
                vbo_dict["texCoords"] += tuple(texture_coords)

                # log_vertex_addition((vertices, texture_coords), (bytes_vertices, bytes_texCoords), len(vbo_dict["vertices"])*4, len(vbo_dict["texCoords"])*4, self.listener.get_queue_length())
            except:
                pass   
        glfw.terminate()

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
        for vbo_data in self.vbos.values():
            if vbo_data["render"]:
                vbo = vbo_data["vbo_vertex"]
                vbo_1 = vbo_data["vbo_texture"]

                glBindBuffer (GL_ARRAY_BUFFER, vbo)
                if not USING_RENDERDOC:
                    glVertexPointer (3, GL_FLOAT, 0, None)
                glBindBuffer(GL_ARRAY_BUFFER, vbo_1)
                if not USING_RENDERDOC:
                    glTexCoordPointer(2, GL_FLOAT, 0, None)

                glDrawArrays (self.mode, 0, VERTICES_SIZE)

        self.timings.append(time.time())
        if len(self.timings) > 10:
            self.timings.pop(0)
            try:
                self.fps = 1 / (self.timings[-1] - self.timings[0])
            except:
                self.fps = 0

class TerrainMeshStorage:
    def __init__(self):
        self.vertices = []
        self.texCoords = []
    
    def add(self, posList, texCoords):
        self.vertices.append(posList)
        self.texCoords.append(texCoords)

    def clear(self):
        self.vertices = []
        self.texCoords = []

    def _group(self):
        to_add = []
        for i in range(0, len(self.vertices), STEP):
            verts = self.vertices[i:i+STEP]
            tex = self.texCoords[i:i+STEP]

            _verts = []
            _tex = []

            for i in verts:
                _verts.extend(i)
            for i in tex:
                _tex.extend(i)

            to_add.append((_verts, _tex))

        return to_add
