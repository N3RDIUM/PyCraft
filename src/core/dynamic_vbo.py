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

    def dispose(self) -> None:
        raise NotImplementedError

BufferList: TypeAlias = list[DisposableBuffer]

class DynamicVBO:
    def __init__(
        self, 
        state: State
    ) -> None:
        self.data: BufferData | None = None
        self.buffers: BufferList = []
        self.state: State = state
        # TODO: actually implementing the dyn part
        # TODO: from that Vercidium vid :P

    @property
    def latest_buffer(self) -> np.uint32 | None:
        return self.buffers[0].buffer

    def set_data(self, data: BufferData) -> None:
        self.data = data
        buffer = DisposableBuffer(data)
        buffer.send_to_gpu(self.state)
        self.buffers.append(buffer)

