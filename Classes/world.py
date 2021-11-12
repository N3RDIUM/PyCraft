import threading
import time
import logging
import math

from Classes.chunk import Chunk

logging.basicConfig(level=logging.DEBUG)


def log(source, message, ctime=None):
    # Get the time in a nice format
    now = time.strftime("%H:%M:%S")
    if ctime is not None:
        now = ctime
    logging.debug(f"({now}) [{source}]: {message}")

class TaskScheduler:
    def __init__(self):
        self.tasks = []
        self.task_lock = threading.Lock()
        self._frame = 0

    def add_task(self, tasklist):
        # Calculate the appropriate frame to run the task
        APPROPRIATE_FRAME = self._frame + 1
        for i in self.tasks:
            if i[1] == APPROPRIATE_FRAME:
                APPROPRIATE_FRAME += 1

        with self.task_lock:
            self.tasks.append([tasklist, APPROPRIATE_FRAME])

    def run(self):
        try:
            for task in self.tasks:
                if task[1] == self._frame:
                    task[0]()
                    del self.tasks[0]
        finally:
            self._frame += 1

class World:
    def __init__(self, Chunk, Player):
        self.CHUNK_DIST = 16
        self.generated = False
        self.Chunk = Chunk
        self.chunk_distance = 2
        self.player = Player

        self.x = 0
        self.z = 0

        self.chunks = self.generate_2d_array(self.chunk_distance*2+1)
        self._scheduler = TaskScheduler()
        self._scheduler_ = TaskScheduler()
        threading.Thread(target=self.generate,daemon=True).start()
        self._tick = 0

    def generate_2d_array(self, size):
        return [[None] * size for _ in range(size)]

    def generate(self):
        self.generated = False
        for i in range(-self.chunk_distance, self.chunk_distance):
            for j in range(-self.chunk_distance, self.chunk_distance):
                self.make_chunk((self.x+i, self.z+j), i+self.chunk_distance)
        self.generated = True

    def draw(self):
        self._tick += 1
        for i in self.chunks:
            for chunk in i:
                if chunk is not None and chunk.generated:
                    chunk.draw()
        if self._tick % 10 == 0:
            self._scheduler.run()
            self._scheduler_.run()

    def make_chunk(self, xz, index):
        chunk = self.Chunk(xz[0], xz[1], self)
        self.chunks[index].append(chunk)
        self._scheduler.add_task(lambda: threading.Thread(target=chunk.generate,daemon=True).start())

    def add_row_z_minus(self):
        self.chunks.append([])
        data = []
        for x in range(-self.chunk_distance, self.chunk_distance):
            data.append(self.Chunk(self.x+x, self.z-self.chunk_distance, self))
            self._scheduler_.add_task(data[-1].generate)
        self.chunks.insert(0, data)
        self.z -= 1

    def add_row_z_plus(self):
        self.chunks.insert(0, [])
        data = []
        for x in range(-self.chunk_distance, self.chunk_distance):
            data.append(self.Chunk(self.x+x, self.z+self.chunk_distance, self))
            self._scheduler_.add_task(data[-1].generate)
        self.chunks.append(data)
        self.z += 1

    def add_row_x_minus(self):
        self.chunks.append([])
        data = []
        for z in range(-self.chunk_distance, self.chunk_distance):
            data.append(self.Chunk(self.x-self.chunk_distance, self.z+z, self))
            self._scheduler_.add_task(data[-1].generate)
        self.chunks.insert(0, data)
        self.x -= 1

    def add_row_x_plus(self):
        self.chunks.append([])
        data = []
        for z in range(-self.chunk_distance, self.chunk_distance):
            data.append(self.Chunk(self.x+self.chunk_distance, self.z+z, self))
            self._scheduler_.add_task(data[-1].generate)
        self.chunks.append(data)
        self.x += 1

    def update(self, dt):
        x = self.player.pos[0]
        z = self.player.pos[2]
        if math.dist([self.x],[z/16]) >= self.chunk_distance-1:
            self.add_row_z_minus()
        elif math.dist([self.x],[z/16]) <= -self.chunk_distance+1:
            self.add_row_z_plus()
        
        if math.dist([x/16],[self.z]) >= self.chunk_distance-1:
            self.add_row_x_minus()
        elif math.dist([x/16],[self.z]) <= -self.chunk_distance+1:
            self.add_row_x_plus()