import threading
from logger import *
from pyglet.gl import *

from Classes.chunk import Chunk
from Classes.environment.cloud_generator import cloud_generator

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
    def __init__(self, window, player):
        self.CHUNK_DIST = 16
        self.generated = False
        self.Chunk = Chunk
        self.chunk_distance = 3
        self.parent = window
        self.cloud_generator = cloud_generator(self)
        self.player = player
        self._all_blocks = {}

        self.x = 0
        self.z = 0

        self.chunks = {}
        self._scheduler = TaskScheduler()
        self._scheduler_ = TaskScheduler()
        self.generate()
        self._tick = 0

    def generate(self):
        self.generated = False
        for i in range(-self.chunk_distance, self.chunk_distance):
            for j in range(-self.chunk_distance, self.chunk_distance):
                self.make_chunk((self.x+i, self.z+j),
                                (i+self.chunk_distance, j+self.chunk_distance))
        self.generated = True

    def draw_cube(self, x, y, z, size):
            glPushMatrix()
            glTranslatef(x, y, z)
            glScalef(size, size, size)
            glBegin(GL_QUADS)
            glVertex3f(1, 1, 1)
            glVertex3f(1, 1, -1)
            glVertex3f(-1, 1, -1)
            glVertex3f(-1, 1, 1)
            glVertex3f(1, -1, 1)
            glVertex3f(1, -1, -1)
            glVertex3f(-1, -1, -1)
            glVertex3f(-1, -1, 1)
            glVertex3f(1, 1, 1)
            glVertex3f(-1, 1, 1)
            glVertex3f(-1, -1, 1)
            glVertex3f(1, -1, 1)
            glVertex3f(1, 1, -1)
            glVertex3f(-1, 1, -1)
            glPopMatrix()

    def draw_player_hitbox(self, pos):
        # Just draw a cube with black outline
        self.draw_cube(pos[0], pos[1], pos[2], 1)

    def draw(self):
        self._tick += 1
        try:
            self.draw_player_hitbox(self.parent.player.looking_at[0])
        except:
            pass
        
        for i in self.chunks:
            chunk = self.chunks[i]
            if chunk is not None and chunk.generated:
                chunk.draw()
        self.cloud_generator.draw()
        self._scheduler.run()
        self._scheduler_.run()

    def make_chunk(self, xz, index):
        chunk = self.Chunk(xz[0], xz[1], self)
        self.chunks[index] = chunk
        chunk.generate()

    def chunk_exists(self, index):
        return index in self.chunks

    def block_exists(self, coords):
        try:
            return self._all_blocks[(coords[0], coords[1], coords[2])].block_data
        except:
            return False

    def add_row_z_minus(self):
        data = {}
        for x in range(-self.chunk_distance, self.chunk_distance):
            if not self.chunk_exists((self.x+x, self.z-self.chunk_distance)):
                data[(self.x+x, self.z-self.chunk_distance)
                     ] = self.Chunk(self.x+x, self.z-self.chunk_distance, self)
                self._scheduler_.add_task(
                    data[self.x+x, self.z-self.chunk_distance].generate)
        for i in data:
            self.chunks[i] = data[i]
        self.z -= 1

    def add_row_z_plus(self):
        data = {}
        for x in range(-self.chunk_distance, self.chunk_distance):
            if not self.chunk_exists((self.x+x, self.z+self.chunk_distance)):
                data[(self.x+x, self.z+self.chunk_distance)
                     ] = self.Chunk(self.x+x, self.z+self.chunk_distance, self)
                self._scheduler_.add_task(
                    data[self.x+x, self.z+self.chunk_distance].generate)
        for i in data:
            self.chunks[i] = data[i]
        self.z += 1

    def add_row_x_minus(self):
        data = {}
        for z in range(-self.chunk_distance, self.chunk_distance):
            if not self.chunk_exists((self.x-self.chunk_distance, self.z+z)):
                data[(self.x-self.chunk_distance, self.z+z)
                     ] = self.Chunk(self.x-self.chunk_distance, self.z+z, self)
                self._scheduler_.add_task(
                    data[self.x-self.chunk_distance, self.z+z].generate)
        for i in data:
            self.chunks[i] = data[i]
        self.x -= 1

    def add_row_x_plus(self):
        data = {}
        for z in range(-self.chunk_distance, self.chunk_distance):
            if not self.chunk_exists((self.x+self.chunk_distance, self.z+z)):
                data[(self.x+self.chunk_distance, self.z+z)
                     ] = self.Chunk(self.x+self.chunk_distance, self.z+z, self)
                self._scheduler_.add_task(
                    data[self.x+self.chunk_distance, self.z+z].generate)
        for i in data:
            self.chunks[i] = data[i]
        self.x += 1

    def _check_no_holes(self):
        for i in range(self.x-self.chunk_distance+1, self.x+self.chunk_distance-1):
            for j in range(self.z-self.chunk_distance+1, self.z+self.chunk_distance-1):
                if not self.chunk_exists((i, j)):
                    self.make_chunk((i, j), (i, j))

    def remove_block(self, coords):
        if self._all_blocks[(coords[0], coords[1], coords[2])].generated:
            self._all_blocks[(coords[0], coords[1], coords[2])].remove()

    def update(self, dt):
        x = int(self.player.pos[0]/self.CHUNK_DIST*2)
        z = int(self.player.pos[2]/self.CHUNK_DIST*2)                
        self._check_no_holes()

        if x != self.x:
            if x+1 > self.x:
                self.add_row_x_plus()
            elif x-1 < self.x:
                self.add_row_x_minus()
        if z != self.z:
            if z+1 > self.z:
                self.add_row_z_plus()
            elif z-1 < self.z:
                self.add_row_z_minus()
