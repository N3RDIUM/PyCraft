import numpy as np
from core.state import State
from core.dynamic_vbo import DynamicVBO
from .block import front, back, left, right, top, bottom

CHUNK_SIDE = 16
CHUNK_DIMS = tuple(CHUNK_SIDE + 2 for _ in range(3)) # Padding of 2 for obvious reasons

def translate(mesh: np.typing.NDArray[np.float32], position: tuple[int, int, int]):
    new = np.array(mesh, dtype=np.float32)
    for i in range(len(mesh)):
        f = i % 3
        new[i] += position[f]
    return new

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
        for x in range(CHUNK_SIDE - 1):
            for y in range(CHUNK_SIDE - 1):
                for z in range(CHUNK_SIDE - 1):
                    self.terrain[x + 1][y + 1][z + 1] = 1

    def append_to_mesh(self, data: np.typing.NDArray[np.float32]) -> None:
        if self.mesh is None:
            self.mesh = data
            return
        self.mesh = np.hstack((self.mesh, data))

    def is_air(self, x: int, y: int, z: int) -> bool:
        return self.terrain[x][y][z] == 0

    def generate_mesh(self) -> None:
        for x in range(CHUNK_SIDE):
            for y in range(CHUNK_SIDE):
                for z in range(CHUNK_SIDE):
                    if self.is_air(x, y, z):
                        continue

                    self.append_to_mesh(translate(front, (x, y, z)))
                    self.append_to_mesh(translate(back, (x, y, z)))
                    self.append_to_mesh(translate(right, (x, y, z)))
                    self.append_to_mesh(translate(left, (x, y, z)))
                    self.append_to_mesh(translate(top, (x, y, z)))
                    self.append_to_mesh(translate(bottom, (x, y, z)))

