from typing import TypeAlias

import numpy as np
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_STATIC_DRAW,
    glBindBuffer,
    glBufferData,
    glBufferSubData,
    glFlush,
    glGenBuffers,
    glDeleteBuffers,
)
from OpenGL.GL import *

from .state import State

BufferData: TypeAlias = np.typing.NDArray[np.float32]

DELETE_UNNEEDED = 0
SEND_TO_GPU = 1
VERTEX = 2
UV = 3

class DisposableBuffer:
    def __init__(self, data: BufferData, type: int = VERTEX) -> None:
        self.data: BufferData = data
        self.type: int = type
        self.buffer: np.uint32 = glGenBuffers(1)
        self.ready: bool = False
        
    def send_to_gpu(self) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.data.nbytes, self.data)
        glFlush()
        self.ready = True

    def __del__(self) -> None:
        glDeleteBuffers(1, self.buffer)
        del self.data

class Mesh:
    def __init__(
        self,
        state: State,
    ) -> None:
        self.buffers = []
        self.state: State = state

    def get_latest_buffer(self) -> np.uint32 | None:
        latest = None
        for buffer in self.buffers:
            if not buffer[0].ready or not buffer[1].ready:
                continue
            latest = buffer
            break
        return latest

    def set_data(self, vertices, uvs) -> None:
        vertex_buf = DisposableBuffer(vertices, VERTEX)
        uv_buf = DisposableBuffer(uvs, UV)
        self.buffers.insert(0, (vertex_buf, uv_buf))

    def render(self) -> None:
        buffers = self.get_latest_buffer()
        if buffers is None:
            return
        vertex, uv = buffers
    
        glBindBuffer(GL_ARRAY_BUFFER, vertex.buffer)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindBuffer(GL_ARRAY_BUFFER, uv.buffer)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)

        glDrawArrays(GL_TRIANGLES, 0, len(vertex.data) // 3)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def update_buffers(self, mode: int = SEND_TO_GPU) -> None:
        for (vertex, uv) in self.buffers:
            if not mode == SEND_TO_GPU:
                continue
            
            if not vertex.ready:
                vertex.send_to_gpu()
            if not uv.ready:
                uv.send_to_gpu()

        if mode != DELETE_UNNEEDED:
            return

            
        to_delete = []
        latest = self.get_latest_buffer()
        for (vertex, uv) in self.buffers:
            if (vertex, uv) == latest:
                continue
            if vertex.ready and uv.ready:
                to_delete.append((vertex, uv))

        for (vertex, uv) in to_delete:
            self.buffers.remove((vertex, uv))
            del vertex
            del uv

    def on_close(self) -> None:
        del self.buffers

MeshStore: TypeAlias = dict[str, Mesh]


class MeshHandler:
    def __init__(self, state: State) -> None:
        self.state: State = state
        self.meshes: MeshStore = {}

        if self.state.mesh_handler is not None:
            raise Exception(
                "[core.dynamic_vbo.DynamicVBOHandler] Tried to create multiple instances of this class"
            )
        self.state.mesh_handler = self

    def new_mesh(self, id: str) -> Mesh:
        buffer = Mesh(self.state)
        self.meshes[id] = buffer
        return buffer

    def get_mesh(self, id: str) -> Mesh:
        return self.meshes[id]
    
    def remove_buffer(self, id: str) -> None:
        del self.meshes[id]

    def drawcall(self) -> None:
        try:
            for mesh in self.meshes:
                self.meshes[mesh].render()
        except RuntimeError:
            pass

    def update(self, mode: int = SEND_TO_GPU) -> None:
        try:
            for mesh in self.meshes:
                self.meshes[mesh].update_buffers(mode)
        except RuntimeError:
            pass
        except IndexError:
            pass

    def on_close(self) -> None:
        try:
            for mesh in self.meshes:
                self.meshes[mesh].on_close()
        except RuntimeError:
            self.on_close()
        except KeyError:
            self.on_close()

