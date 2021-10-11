import threading

class PrepareBatch(threading.Thread):
    def __init__(self, world, xztuple):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.world = world
        self.xztuple = xztuple
        self.start()

    def start(self):
        try:
            self.c = self.world.Chunk(self.xztuple[0], self.xztuple[1],self.world)
            self.c.generate()
            self.world.temp.append(self.c)
            exit()
        except Exception as e:
            print("Failed to generate chunk", self.xztuple, f"\n{e}")
            exit()

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
        self.temp = []

    def generate(self):
        self.generating = False
        self.chunks = []
        for i in range(-self.chunk_distance, self.chunk_distance):
            self.temp = []
            for j in range(-self.chunk_distance, self.chunk_distance):
                try:
                    PrepareBatch(self, (self.x+i, self.z+j))
                except:
                    pass
            self.chunks.append(self.temp)

    def draw(self):
        for i in self.chunks:
            for chunk in i:
                chunk.draw()

    def update(self, dt):
        x = int(self.player.pos[0]/16)
        z = int(self.player.pos[2]/16)
        if x != self.x or z != self.z:
            self.x = x
            self.z = z
            self.generate()
