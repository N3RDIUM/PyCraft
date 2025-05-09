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

from .state import State

DELETE_UNNEEDED = 0
SEND_TO_GPU = 1

BufferData: TypeAlias = np.typing.NDArray[np.float32]


class DisposableBuffer:
    def __init__(self, data: BufferData) -> None:
        self.data: BufferData = data
        self.buffer: np.uint32 = glGenBuffers(1)
        self.ready_frame: int | None = None

    def send_to_gpu(self, state: State) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        glBufferData(GL_ARRAY_BUFFER, self.data.nbytes, None, GL_STATIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.data.nbytes, self.data)
        glFlush()
        self.ready_frame = state.frame

    @property
    def ready(self) -> bool:
        return self.ready_frame is not None

    def __del__(self) -> None:
        glDeleteBuffers(1, self.buffer)
        del self.data

BufferList: TypeAlias = list[DisposableBuffer]


class DynamicVBO:
    def __init__(
        self,
        state: State,
    ) -> None:
        self.data: BufferData | None = None
        self.buffers: BufferList = []
        self.state: State = state
        self.visible: bool = True

    @property
    def latest_buffer(self) -> np.uint32 | None:
        latest: np.uint32 | None = None
        for buffer in self.buffers:
            if not buffer.ready:
                continue
            latest = buffer.buffer
            break
        return latest

    def set_data(self, data: BufferData) -> None:
        self.data = data
        buffer = DisposableBuffer(data)
        self.buffers.append(buffer)

    def update_buffers(self, mode: int = SEND_TO_GPU) -> None:
        ready_buffer_count: int = 0
        for i in range(len(self.buffers)):
            if not self.buffers[i].ready and mode == SEND_TO_GPU:
                self.buffers[i].send_to_gpu(self.state)
                continue

            if mode != DELETE_UNNEEDED:
                continue
            ready_buffer_count += 1
            if ready_buffer_count > 1:
                del self.buffers[i]

    def on_close(self) -> None:
        for i in range(len(self.buffers)):
            del self.buffers[i]

DynamicBufferStore: TypeAlias = dict[str, DynamicVBO]


class DynamicVBOHandler:
    def __init__(self, state: State) -> None:
        self.state: State = state
        self.vbos: DynamicBufferStore = {}

        if self.state.vbo_handler is not None:
            raise Exception(
                "[core.dynamic_vbo.DynamicVBOHandler] Tried to create multiple instances of this class"
            )
        self.state.vbo_handler = self

    def new_buffer(self, id: str) -> DynamicVBO:
        buffer = DynamicVBO(self.state)
        self.vbos[id] = buffer
        return buffer

    def get_buffer(self, id: str) -> DynamicVBO:
        return self.vbos[id]
    
    def all_buffers(self):
        return self.vbos.values()

    def remove_buffer(self, id: str) -> None:
        del self.vbos[id]

    def update(self, mode: int = SEND_TO_GPU) -> None:
        for vbo in self.vbos:
            self.vbos[vbo].update_buffers(mode)

    def on_close(self) -> None:
        for vbo in self.vbos:
            self.vbos[vbo].on_close()

