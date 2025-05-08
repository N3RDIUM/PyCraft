import numpy as np
from core.state import State
from core.dynamic_vbo import DynamicVBO

CHUNK_SIDE = 16


class Chunk:
    def __init__(self, position: list[int], state: State):
        self.state: State = state
        self.position: list[int] = position

        self.terrain: np.typing.NDArray[np.uint64] = np.zeros(
            tuple(CHUNK_SIDE for _ in range(3)), dtype=np.uint64
        )
        self.buffer: DynamicVBO = self.state.vbo_handler.new_buffer(self.id)

    @property
    def id(self) -> str:
        return f"chunk_{self.position[0]}_{self.position[1]}"
