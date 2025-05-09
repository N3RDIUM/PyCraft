from .chunk import Chunk, CHUNK_SIDE
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

    def update(self) -> None:
        # WORLD: Impl global block_exists func. Gen in 2 stages: terrain gen all then mesh gen all
        required_chunks = []
        player_position = self.state.camera.position
        camera_chunk = list((int(player_position[i] // (CHUNK_SIDE - 1)) for i in range(3)))
        for x in range(-RENDER_DIST, RENDER_DIST + 1):
            for z in range(-RENDER_DIST, RENDER_DIST + 1):
                translated_x = x - camera_chunk[0]
                translated_z = z - camera_chunk[2]
                required_chunks.append((translated_x, -1, translated_z))

        for required in required_chunks:
            if required not in list(self.chunks.keys()):
                chunk = Chunk(required)
                self.chunks[required] = chunk

        to_delete = []
        for chunk in list(self.chunks.keys()):
            if chunk not in required_chunks:
                to_delete.append(chunk)
        
        for chunk in to_delete:
            del self.chunks[chunk]

        for id in self.chunks:
            chunk = self.chunks[id]

            if chunk.generated: # In 2-stage gen: status instead of generated
                continue

            self.chunks[id].generate()

            self.update_mesh()

    def update_mesh(self) -> None:
        vertices = []
        uvs = []
        for id in list(self.chunks.keys()):
            chunk = self.chunks[id]

            if not chunk.generated:
                continue
            
            vertices.append(chunk.vertices)
            uvs.append(chunk.uvs)
    
        vertices = np.hstack(tuple(vertices))
        uvs = np.hstack(tuple(uvs))

        self.mesh.set_data(vertices, uvs)

