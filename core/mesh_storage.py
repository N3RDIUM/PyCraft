STEP = 512

class TerrainMeshStorage:
    def __init__(self):
        self.vertices = []
        self.texCoords = []
    
    def add(self, posList, texCoords):
        self.vertices.append(posList)
        self.texCoords.append(texCoords)

    def clear(self):
        self.vertices = []
        self.texCoords = []

    def _group(self):
        to_add = []
        for i in range(0, len(self.vertices), STEP):
            verts = self.vertices[i:i+STEP]
            tex = self.texCoords[i:i+STEP]

            _verts = []
            _tex = []

            for i in verts:
                _verts.extend(i)
            for i in tex:
                _tex.extend(i)

            to_add.append((_verts, _tex))

        return to_add
