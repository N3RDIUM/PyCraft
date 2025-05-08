import numpy as np
from core.state import State

CHUNK_SIDE = 16


class Chunk:
    def __init__(self, state: State):
        self.state: State = state
        self.terrain: np.typing.NDArray[np.uint64] = np.zeros(
            tuple(CHUNK_SIDE for _ in range(3)), dtype=np.uint64
        )

