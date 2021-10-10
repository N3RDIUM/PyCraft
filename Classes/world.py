import threading


class World:
    def __init__(self, Chunk, Player):
        self.generating = False
        self.chunks = []
        self.Chunk = Chunk
        self.chunk_distance = 3
        self.player = Player

        self.x = 0
        self.z = 0

        self.generate()

    def generate(self):
        self.generating = False
        self.chunks = []
        for i in range(-self.chunk_distance, self.chunk_distance):
            temp = []
            for j in range(-self.chunk_distance, self.chunk_distance):
                try:
                    c = self.Chunk(i+self.x, j+self.z, self)
                    c.generate()
                    temp.append(c)
                except:
                    pass
            self.chunks.append(temp)

    def draw(self):
        for i in self.chunks:
            for chunk in i:
                chunk.draw()

    def update(self, dt):
        x = self.player.pos[0]
        z = self.player.pos[2]

        # Nothin' to do with this
        dt

        if x > self.x*16 + self.chunk_distance-1:
            self.x += 1
            self.generate()
        elif x < self.x*16 - self.chunk_distance-1:
            self.x -= 1
            self.generate()
        elif z > self.z*16 + self.chunk_distance-1:
            self.z += 1
            self.generate()
        elif z < self.z*16 - self.chunk_distance-1:
            self.z -= 1
            self.generate()
