from OpenGL.arrays.vbo import VBO
from typing import TypeAlias
import numpy as np
from .state import State

BufferData: TypeAlias = np.typing.NDArray[np.float32]

class DisposableBuffer:
    def __init__(self, data: BufferData) -> None:
        self.data: BufferData = data
        self.buffer: VBO | None = None

    def send_to_gpu(self) -> None:
        self.buffer = VBO(self.data)

    def dispose(self) -> None:
        if self.buffer is not None:
            self.buffer.delete()

BufferList: TypeAlias = list[DisposableBuffer]

class DynVBO:
    def __init__(
        self, 
        state: State
    ) -> None:
        self.data: BufferData | None = None
        self.buffers: BufferList = []
        self.state: State = state
        # TODO: actually implementing the dyn part
        # TODO: from that Vercidium vid :P

    def get_latest_buffer(self) -> VBO | None:
        return self.buffers[0].buffer

    def set_data(self, data: BufferData) -> None:
        self.data = data
        buffer = DisposableBuffer(data)
        buffer.send_to_gpu()
        self.buffers.append(buffer)

