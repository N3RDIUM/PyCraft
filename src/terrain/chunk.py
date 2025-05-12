import numpy as np
from .block import front, back, left, right, top, bottom, uv
import noise

CHUNK_SIDE = 16
CHUNK_DIMS = tuple(CHUNK_SIDE + 2 for _ in range(3))  # Padding of 2 for "obvious reasons"
FACES = [
    ((0, 0, 1), front.reshape((6, 3))),
    ((0, 0, -1), back.reshape((6, 3))),
    ((-1, 0, 0), right.reshape((6, 3))),
    ((1, 0, 0), left.reshape((6, 3))),
    ((0, -1, 0), top.reshape((6, 3))),
    ((0, 1, 0), bottom.reshape((6, 3))),
]

NOT_GENERATED = 0
TERRAIN_GENERATED = 1
MESH_GENERATED = 2

class Chunk:
    def __init__(self, position: tuple[int, int, int]):
        self.position = position
        self.state = NOT_GENERATED

        self.terrain: np.typing.NDArray[np.uint8] = np.zeros(
            CHUNK_DIMS, dtype=np.uint8
        )
        self.vertices: np.typing.NDArray[np.float32] | None = None
        self.uvs: np.typing.NDArray[np.float32] | None = None

    @property
    def id(self) -> str:
        return f"chunk_{self.position[0]}_{self.position[1]}_{self.position[2]}"

    def is_air(self, x: int, y: int, z: int) -> bool:
        return self.terrain[x, y, z] == 0

    def update_neighbour_terrain(self, world):
        neighbour_dirs = {
            (1, 0, 0): (slice(-1, None), slice(1, -1), slice(1, -1)),  
            (-1, 0, 0): (slice(0, 1), slice(1, -1), slice(1, -1)),     
            (0, 1, 0): (slice(1, -1), slice(-1, None), slice(1, -1)),  
            (0, -1, 0): (slice(1, -1), slice(0, 1), slice(1, -1)),     
            (0, 0, 1): (slice(1, -1), slice(1, -1), slice(-1, None)),  
            (0, 0, -1): (slice(1, -1), slice(1, -1), slice(0, 1)),     
        }

        center = (slice(1, -1), slice(1, -1), slice(1, -1))

        for (dx, dy, dz), dest_slice in neighbour_dirs.items():
            neighbor_pos = (self.position[0] + dx, self.position[1] + dy, self.position[2] + dz)
            if world.chunk_exists(neighbor_pos):
                neighbor = world.chunks[neighbor_pos]
                if dx == 1:  
                    source = (slice(1, 2),) + center[1:]
                elif dx == -1:  
                    source = (slice(-2, -1),) + center[1:]
                elif dy == 1:  
                    source = (center[0], slice(1, 2), center[2])
                elif dy == -1:  
                    source = (center[0], slice(-2, -1), center[2])
                elif dz == 1:
                    source = center[:2] + (slice(1, 2),)
                elif dz == -1:
                    source = center[:2] + (slice(-2, -1),)

                self.terrain[dest_slice] = neighbor.terrain[source]

    def generate_terrain(self) -> None:
        for i in range(CHUNK_SIDE):
            for j in range(CHUNK_SIDE):
                x, z = i + 1, j + 1
                relative_y = self.position[1] * (CHUNK_SIDE - 1)
                translated = (
                    (x + self.position[0] * (CHUNK_SIDE - 1)) / 1000,
                    (z + self.position[2] * (CHUNK_SIDE - 1)) / 1000,
                )
                terrain_height = noise.snoise2(*translated) * 100
                terrain_height += noise.snoise2(*(translated[i] * 10 for i in [0, 1])) * 10
                terrain_height = int(terrain_height - relative_y)

                if terrain_height >= 0 and terrain_height <= CHUNK_SIDE:
                    for k in range(terrain_height):
                        self.terrain[x, k, z] = 1
                elif terrain_height > CHUNK_SIDE:
                    self.terrain[x, :, z] = 1

                for l in range(CHUNK_SIDE):
                    y = l + 1
                    translated = (
                        (x + self.position[0] * (CHUNK_SIDE - 1)) / 100,
                        (y + self.position[1] * (CHUNK_SIDE - 1)) / 100,
                        (z + self.position[2] * (CHUNK_SIDE - 1)) / 100,
                    )
                    cave_noise = noise.snoise3(*translated)
                    if cave_noise > 0.3:
                        self.terrain[x, y, z] = 0
                    
        self.state = TERRAIN_GENERATED

    def generate_mesh(self, world) -> None:
        if not np.any(self.terrain[1:-1, 1:-1, 1:-1]):
            self.vertices = np.array([], dtype=np.float32)
            self.uvs = np.array([], dtype=np.float32)
            self.state = MESH_GENERATED
            return

        self.update_neighbour_terrain(world)
        offset = np.array(self.position) * (CHUNK_SIDE - 1)
        solid = self.terrain[1:-1, 1:-1, 1:-1] != 0

        face_data = []
        total_faces = 0

        for (dx, dy, dz), face in FACES:
            neighbor = self.terrain[
                1 + dx : -1 + dx or None,
                1 + dy : -1 + dy or None,
                1 + dz : -1 + dz or None
            ]

            visible = solid & (neighbor == 0)
            if not np.any(visible):
                continue

            x, y, z = np.where(visible)
            positions = np.stack((x + 1, y + 1, z + 1), axis=1).astype(np.float32) + offset
            translated_faces = face[np.newaxis, :, :] + positions[:, np.newaxis, :]
            face_data.append(translated_faces.reshape(-1))
            total_faces += positions.shape[0]

        if face_data:
            self.vertices = np.hstack(face_data).astype(np.float32)
            self.uvs = np.tile(uv, (total_faces, 1)).reshape(-1).astype(np.float32)
        else:
            self.vertices = np.array([], dtype=np.float32)
            self.uvs = np.array([], dtype=np.float32)

        self.state = MESH_GENERATED

