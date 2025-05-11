from .chunk import Chunk, CHUNK_SIDE, TERRAIN_GENERATED, MESH_GENERATED
from core.state import State
from core.mesh import Mesh
import numpy as np
import multiprocessing

RENDER_DIST = 8
RENDER_HEIGHT = 4

# TODO: Full rewrite. Do everything chunk-related on the worker process.
# TODO: All the main thread's World class has to touch is the mesh data,
# TODO: passed through a queue. The only thing the World gives the
# TODO: worker process is the player position.

class ChunkStorage:
    def __init__(self) -> None:
        self.chunks = {}
        self.changed = False

    def add_chunk(self, chunk):
        self.chunks[chunk.position] = chunk
        self.changed = True

    def chunk_exists(self, position) -> bool:
        return position in self.chunks

    def get_neighbours(self, id) -> list[Chunk]:
        x, y, z = id
        directions = [
            (1, 0, 0), (-1, 0, 0),
            (0, 1, 0), (0, -1, 0),
            (0, 0, 1), (0, 0, -1),
        ]
        
        neighbours = []
        for dx, dy, dz in directions:
            neighbour_id = (x + dx, y + dy, z + dz)
            if neighbour_id in self.chunks:
                neighbours.append(self.chunks[neighbour_id])
        
        return neighbours
    
    def generate(self):
        for id in self.chunks:
            if self.chunks[id].state == TERRAIN_GENERATED:
                continue
            self.chunks[id].generate_terrain()

        for id in self.chunks:
            if self.chunks[id].state != TERRAIN_GENERATED:
                continue
            self.chunks[id].generate_mesh(self)

        self.changed = False

    def generate_mesh_data(self):
        vertices = []
        uvs = []

        for id in list(self.chunks.keys()):
            chunk = self.chunks[id]

            if chunk.state != MESH_GENERATED:
                continue
            
            vertices.append(chunk.vertices)
            uvs.append(chunk.uvs)
        
        try:
            vertices = np.hstack(vertices)
            uvs = np.hstack(uvs)
            return (vertices, uvs)
        except ValueError:
            return None

class ChunkHandler:
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.namespace = self.manager.Namespace()
        self.namespace.mesh_data = None
        self.namespace.changed = False

        self.process = multiprocessing.Process(
            target=self.worker,
            args=(self.namespace, )
        )
        self.process.start()

    def worker(self, namespace):
        storage = ChunkStorage()
        chunk = Chunk((0, 0, 0))
        storage.add_chunk(chunk)

        while True:
            if not storage.changed:
                continue
            storage.generate()
            namespace.mesh_data = storage.generate_mesh_data()
            namespace.changed = True

    @property
    def mesh_data(self):
        self.namespace.changed = False
        return self.namespace.mesh_data

    @property
    def changed(self):
        return self.namespace.changed

class World:
    def __init__(self, state: State) -> None:
        self.state: State = state
        self.handler = ChunkHandler()
        self.state.world = self
        self.mesh: Mesh = self.state.mesh_handler.new_mesh("world")

    def update(self) -> None:
        if not self.handler.changed:
            return

        data = self.handler.mesh_data
        if data is None:
            return
        
        self.mesh.set_data(*data)

