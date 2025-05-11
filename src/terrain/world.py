from .chunk import Chunk, CHUNK_SIDE, TERRAIN_GENERATED, MESH_GENERATED
from core.state import State
from core.mesh import Mesh
import numpy as np
import multiprocessing

RENDER_DIST = 8
RENDER_HEIGHT = 1

class ChunkStorage:
    def __init__(self) -> None:
        self.chunks = {}
        self.changed = False

    def add_chunk(self, chunk):
        self.chunks[chunk.position] = chunk
        self.changed = True
    
    def delete_chunk(self, position):
        del self.chunks[position]
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

    def update(self, camera_chunk):
        required_chunks = []

        for x in range(-RENDER_DIST - 1, RENDER_DIST):
            for z in range(-RENDER_DIST - 1, RENDER_DIST):
                translated_x = x - camera_chunk[0]
                translated_y = -1
                translated_z = z - camera_chunk[2]
                required_chunks.append((translated_x, translated_y, translated_z))

        for required in required_chunks:
            if required not in list(self.chunks.keys()):
                chunk = Chunk(required)
                self.add_chunk(chunk)

        to_delete = []
        for chunk in list(self.chunks.keys()):
            if chunk not in required_chunks:
                to_delete.append(chunk)
        
        for chunk in to_delete:
            self.delete_chunk(chunk)

class ChunkHandler:
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.namespace = self.manager.Namespace()
        self.namespace.mesh_data = None
        self.namespace.changed = False
        self.namespace.camera_chunk = (0, 0, 0)
        self.namespace.alive = True

        self.process = multiprocessing.Process(
            target=self.worker,
            args=(self.namespace, )
        )
        self.process.start()

    def worker(self, namespace):
        storage = ChunkStorage()

        while self.namespace.alive:
            storage.update(namespace.camera_chunk)

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

    def set_camera_chunk(self, position):
        self.namespace.camera_chunk = position

    def kill(self):
        self.namespace.alive = False
        self.process.terminate()

class World:
    def __init__(self, state: State) -> None:
        self.state: State = state
        self.handler = ChunkHandler()
        self.state.world = self
        self.mesh: Mesh = self.state.mesh_handler.new_mesh("world")

    def update(self) -> None:
        player_position = self.state.camera.position
        camera_chunk = tuple((int(player_position[i] // (CHUNK_SIDE - 1)) for i in range(3)))
        self.handler.set_camera_chunk(camera_chunk)

        if not self.handler.changed:
            return

        data = self.handler.mesh_data
        if data is None:
            return
        
        self.mesh.set_data(*data)

    def on_close(self):
        self.handler.kill()

