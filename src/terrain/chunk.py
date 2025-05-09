import numpy as np
from core.state import State
from core.dynamic_vbo import DynamicVBO
from .block import front, back, left, right, top, bottom

CHUNK_SIDE = 16
CHUNK_DIMS = tuple(CHUNK_SIDE + 2 for _ in range(3))  # Padding of 2 for "obvious reasons"

class Chunk:
    def __init__(self, position: list[int], state: State):
        self.state: State = state
        self.position: list[int] = position

        self.terrain: np.typing.NDArray[np.uint64] = np.zeros(
            CHUNK_DIMS, dtype=np.uint64
        )
        self.mesh: np.typing.NDArray[np.float32] | None = None
        self.buffer: DynamicVBO = self.state.vbo_handler.new_buffer(self.id)

        self.generate_terrain()
        self.generate_mesh()
        self.buffer.set_data(self.mesh)

    @property
    def id(self) -> str:
        return f"chunk_{self.position[0]}_{self.position[1]}_{self.position[2]}"

    def generate_terrain(self) -> None:
        for i in range((CHUNK_SIDE - 1) ** 3):
            x = i % (CHUNK_SIDE - 1)
            y = (i // (CHUNK_SIDE - 1)) % (CHUNK_SIDE - 1)
            z = i // ((CHUNK_SIDE - 1) ** 2)
            self.terrain[x + 1][y + 1][z + 1] = 1

    def append_to_mesh(self, data: np.typing.NDArray[np.float32]) -> None:
        if self.mesh is None:
            self.mesh = data
            return
        self.mesh = np.hstack((self.mesh, data))

    def is_air(self, x: int, y: int, z: int) -> bool:
        return self.terrain[x][y][z] == 0

    def generate_mesh(self) -> None:
        def translate(x, y, z):
            return np.array([[x, y, z] for _ in range(6)], dtype=np.float32).flatten()

        for i in range(CHUNK_SIDE ** 3):
            x = i % CHUNK_SIDE
            y = (i // CHUNK_SIDE) % CHUNK_SIDE
            z = i // (CHUNK_SIDE * CHUNK_SIDE)

            if self.is_air(x, y, z):
                continue

            if self.is_air(x, y, z + 1):
                self.append_to_mesh(front + translate(x, y, z + 1))
            if self.is_air(x, y, z - 1):
                self.append_to_mesh(back + translate(x, y, z - 1))
            if self.is_air(x - 1, y, z):
                self.append_to_mesh(right + translate(x - 1, y, z))
            if self.is_air(x + 1, y, z):
                self.append_to_mesh(left + translate(x + 1, y, z))
            if self.is_air(x, y - 1, z):
                self.append_to_mesh(top + translate(x, y - 1, z))
            if self.is_air(x, y + 1, z):
                self.append_to_mesh(bottom + translate(x, y + 1, z))

