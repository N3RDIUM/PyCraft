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
    glDeleteBuffers
)

from .state import State

BufferData: TypeAlias = np.typing.NDArray[np.float32]

class DisposableBuffer:
    def __init__(self, data: BufferData) -> None:
        self.data: BufferData = data
        self.buffer: np.uint32 = glGenBuffers(1)
        self.ready_frame: int | None = None

    def send_to_gpu(self, state: State) -> None:
        glBindBuffer(GL_ARRAY_BUFFER, self.buffer)
        glBufferData(
            GL_ARRAY_BUFFER, 
            self.data.nbytes,
            None, 
            GL_STATIC_DRAW
        )
        glBufferSubData(
            GL_ARRAY_BUFFER,
            0,
            self.data.nbytes,
            self.data
        )
        glFlush()
        self.ready_frame = state.frame

    @property
    def ready(self) -> bool:
        return self.ready_frame is not None

    def __del__(self) -> None:
        del self.data
        glDeleteBuffers(1, self.buffer)

BufferList: TypeAlias = list[DisposableBuffer]

class DynamicVBO:
    def __init__(
        self, 
        state: State,
    ) -> None:
        self.data: BufferData | None = None
        self.buffers: BufferList = []
        self.state: State = state

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
        buffer.send_to_gpu(self.state)
        self.buffers.insert(0, buffer)

    def update_buffers(self) -> None:
        ready: int = 0
        for i in range(len(self.buffers) - 1):
            if not self.buffers[i].ready:
                continue
            ready += 1
            if ready > 1:
                del self.buffers[i]

