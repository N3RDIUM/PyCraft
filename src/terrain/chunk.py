import numpy as np
from core.state import State
from core.mesh import Mesh
from .block import front, back, left, right, top, bottom, uv

CHUNK_SIDE = 16
CHUNK_DIMS = tuple(CHUNK_SIDE + 2 for _ in range(3))  # Padding of 2 for "obvious reasons"

class Chunk:
    def __init__(self, position: list[int]):
        self.position: list[int] = position
        self.generated: bool = False

        self.terrain: np.typing.NDArray[np.uint64] = np.zeros(
            CHUNK_DIMS, dtype=np.uint64
        )
        self.vertices: np.typing.NDArray[np.float32] | None = None
        self.uvs: np.typing.NDArray[np.float32] | None = None

    @property
    def id(self) -> str:
        return f"chunk_{self.position[0]}_{self.position[1]}_{self.position[2]}"

    def append_to_vertices(self, data: np.typing.NDArray[np.float32]) -> None:
        if self.vertices is None:
            self.vertices = data
            return
        self.vertices = np.hstack((self.vertices, data))

    def append_to_uv(self, data: np.typing.NDArray[np.float32]) -> None:
        if self.uvs is None:
            self.uvs = data
            return
        self.uvs = np.hstack((self.uvs, data))

    def is_air(self, x: int, y: int, z: int) -> bool:
        return self.terrain[x][y][z] == 0

    def generate(self) -> None:
        for i in range((CHUNK_SIDE - 1) ** 3):
            x = i % (CHUNK_SIDE - 1)
            y = (i // (CHUNK_SIDE - 1)) % (CHUNK_SIDE - 1)
            z = i // ((CHUNK_SIDE - 1) ** 2)
            self.terrain[x + 1][y + 1][z + 1] = 1

        def translate(x, y, z):
            return np.array([np.array([x, y, z]) + np.array(self.position) * (CHUNK_SIDE - 1) for _ in range(6)], dtype=np.float32).flatten()

        for i in range(CHUNK_SIDE ** 3):
            x = i % CHUNK_SIDE
            y = (i // CHUNK_SIDE) % CHUNK_SIDE
            z = i // (CHUNK_SIDE * CHUNK_SIDE)

            if self.is_air(x, y, z):
                continue

            if self.is_air(x, y, z + 1):
                self.append_to_vertices(front + translate(x, y, z))
                self.append_to_uv(uv)
            if self.is_air(x, y, z - 1):
                self.append_to_vertices(back + translate(x, y, z))
                self.append_to_uv(uv)
            if self.is_air(x - 1, y, z):
                self.append_to_vertices(right + translate(x, y, z))
                self.append_to_uv(uv)
            if self.is_air(x + 1, y, z):
                self.append_to_vertices(left + translate(x, y, z))
                self.append_to_uv(uv)
            if self.is_air(x, y - 1, z):
                self.append_to_vertices(top + translate(x, y, z))
                self.append_to_uv(uv)
            if self.is_air(x, y + 1, z):
                self.append_to_vertices(bottom + translate(x, y, z))
                self.append_to_uv(uv)

        self.generated = True

