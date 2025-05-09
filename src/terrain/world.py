from .chunk import Chunk
from core.state import State
from core.mesh import Mesh
import numpy as np

RENDER_DIST = 4

class World:
    def __init__(self, state: State) -> None:
        self.state: State = state
        self.state.world = self

        self.chunks = {}
        self.mesh: Mesh = self.state.mesh_handler.new_mesh("world")

        for x in range(-RENDER_DIST, RENDER_DIST + 1):
            for z in range(-RENDER_DIST, RENDER_DIST + 1):
                chunk = Chunk([x, -1, z])
                self.chunks[chunk.id] = chunk

    def drawcall(self) -> None:
        pass

    def update(self) -> None:
        for id in self.chunks:
            chunk = self.chunks[id]

            if chunk.generated:
                continue

            self.chunks[id].generate()

        self.update_mesh()

    def update_mesh(self) -> None:
        vertices = []
        uvs = []
        for id in self.chunks:
            chunk = self.chunks[id]

            if not chunk.generated:
                continue
            
            vertices.append(chunk.vertices)
            uvs.append(chunk.uvs)
    
        vertices = np.hstack(tuple(vertices))
        uvs = np.hstack(tuple(uvs))

        self.mesh.set_data(vertices, uvs)

