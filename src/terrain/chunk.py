import numpy as np
from .block import front, back, left, right, top, bottom, uv

CHUNK_SIDE = 16
CHUNK_DIMS = tuple(CHUNK_SIDE + 2 for _ in range(3))  # Padding of 2 for "obvious reasons"
FACES = [
    ((0, 0, 1), front),
    ((0, 0, -1), back),
    ((-1, 0, 0), right),
    ((1, 0, 0), left),
    ((0, -1, 0), top),
    ((0, 1, 0), bottom),
]

class Chunk:
    def __init__(self, position: list[int]):
        self.position: list[int] = position
        self.generated: bool = False

        self.terrain: np.typing.NDArray[np.uint8] = np.random.randint(
            low=0, high=2, size=CHUNK_DIMS, dtype=np.uint8
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
        return self.terrain[x, y, z] == 0

    def generate(self) -> None:
        offset = np.array(self.position) * (CHUNK_SIDE - 1)
        solid = self.terrain[1:-1, 1:-1, 1:-1] != 0
        face_data = []
        total_faces = 0

        neighbors = {
            (0, 0, 1): self.terrain[1:-1, 1:-1, 2:],    # front
            (0, 0, -1): self.terrain[1:-1, 1:-1, :-2],  # back
            (-1, 0, 0): self.terrain[:-2, 1:-1, 1:-1],  # right
            (1, 0, 0): self.terrain[2:, 1:-1, 1:-1],    # left
            (0, -1, 0): self.terrain[1:-1, :-2, 1:-1],  # top
            (0, 1, 0): self.terrain[1:-1, 2:, 1:-1],    # bottom
        }

        for (dx, dy, dz), face in FACES:
            neighbor = neighbors[(dx, dy, dz)]
            visible = (solid & (neighbor == 0))
            visible_indices = np.argwhere(visible) + 1
            if visible_indices.shape[0] == 0:
                continue

            positions = visible_indices.astype(np.float32) + offset
            face = face.reshape((6, 3))
            translated_faces = face[np.newaxis, :, :] + positions[:, np.newaxis, :]
            face_data.append(translated_faces.reshape(-1))
            total_faces += positions.shape[0]

        if face_data:
            self.vertices = np.hstack(face_data).astype(np.float32)
            self.uvs = np.tile(uv, (total_faces, 1)).reshape(-1).astype(np.float32)
        else:
            self.vertices = np.array([], dtype=np.float32)
            self.uvs = np.array([], dtype=np.float32)

        self.generated = True

