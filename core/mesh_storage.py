import multiprocessing
STEP = 4096 * (multiprocessing.cpu_count() // 4)

class TerrainMeshStorage:
    def __init__(self):
        self.vertices = []
        self.texCoords = []
        self.groups = []

    def add(self, posList, texCoords):
        self.vertices.extend(posList)
        self.texCoords.extend(texCoords)

        if len(self.vertices) >= STEP:
            self.groups.append((self.vertices, self.texCoords))
            self.clear()

    def clear(self):
        self.vertices = []
        self.texCoords = []

    def _group(self):
        self.groups.append((self.vertices, self.texCoords))
        self.clear()
        return self.groups
