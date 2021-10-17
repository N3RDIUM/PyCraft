import threading
import time
import logging

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

    def add_task(self, task):
        # Calculate the appropriate frame to run the task
        APPROPRIATE_FRAME = self._frame + 2
        for i in self.tasks:
            if i[1] == APPROPRIATE_FRAME:
                APPROPRIATE_FRAME += 2

        with self.task_lock:
            self.tasks.append([task, APPROPRIATE_FRAME])

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
        self.generated = False
        self.Chunk = Chunk
        self.chunk_distance = 3
        self.player = Player

        self.x = 0
        self.z = 0

        self.chunks = self.generate_2d_array(self.chunk_distance*2+1)
        self._scheduler = TaskScheduler()
        self.generate()

    def generate_2d_array(self, size):
        return [[None] * size for _ in range(size)]

    def generate(self):
        self.generated = False
        for i in range(-self.chunk_distance, self.chunk_distance):
            for j in range(-self.chunk_distance, self.chunk_distance):
                self.make_chunk((self.x+i, self.z+j), (i+self.chunk_distance, j+self.chunk_distance))
        self.generated = True

    def draw(self):
        for i in self.chunks:
            for chunk in i:
                if chunk is not None:
                    chunk.draw()
        self._scheduler.run()

    def make_chunk(self, xz, index):
        self.chunks[index[0]].append(self.Chunk(xz[0], xz[1], self))
        self._scheduler.add_task(self.chunks[index[0]][len(self.chunks[index[0]])-1].generate)

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