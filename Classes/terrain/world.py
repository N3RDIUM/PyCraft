# imports
import threading
from logger import *
from pyglet.gl import *

from Classes.terrain.chunk import *
from Classes.environment.cloud_generator import CloudGenerator

# Task Scheduler Class
class TaskScheduler:
    def __init__(self):
        """
        TaskScheduler

        * The task scheduler class
        """
        self.tasks = []
        self.task_lock = threading.Lock()
        self._frame = 0

    def add_task(self, tasklist):
        """
        add_task

        * Adds a task to the task scheduler.

        :tasklist: The tasks to add.
        """
        # Calculate the appropriate frame to run the task
        APPROPRIATE_FRAME = self._frame + 1
        for i in self.tasks:
            if i[1] == APPROPRIATE_FRAME:
                APPROPRIATE_FRAME += 1

        with self.task_lock:
            self.tasks.append([tasklist, APPROPRIATE_FRAME])

    def run(self):
        """
        run

        * Runs the task scheduler.
        """
        try:
            for task in self.tasks:
                if task[1] == self._frame:
                    task[0]()
                    del self.tasks[0]
        finally:
            self._frame += 1


class World:
    def __init__(self, window, player):
        """
        World

        * The world class.

        :window: The window to draw to.
        :player: The player to draw the world around.
        """
        self.CHUNK_DIST = 16
        self.generated = False
        self.chunk_distance = 3
        self.parent = window
        self.cloud_generator = CloudGenerator(self)
        self.player = player
        self._all_blocks = {}
        self._all_structures = {}

        self.x = 0
        self.z = 0

        self.chunks = {}
        self._scheduler = TaskScheduler()
        self._scheduler_ = TaskScheduler()
        self.generate()
        self._tick = 0

        self.light_color = [5,5,5,5]
        self.daynight_min = 1
        self.daynight_max = 5
        self.light_change = 0.1

    def get_chunk(self, coords):
        """
        get_chu

        * Gets a chunk.

        :coords: The coordinates of the chunk.

        :returns: The chunk.
        """
        return self.chunks[(coords[0], coords[1])]

    def generate(self):
        """
        generate

        * Generates the world.
        """
        self.generated = False
        for i in range(-self.chunk_distance, self.chunk_distance):
            for j in range(-self.chunk_distance, self.chunk_distance):
                self.make_chunk((self.x+i, self.z+j),
                                (i+self.chunk_distance, j+self.chunk_distance))
        self.generated = True

    @staticmethod
    def draw_cube(x, y, z, size):
        """
        draw_cube

        * Draws a cube.

        :x: The x coordinate of the cube.
        :y: The y coordinate of the cube.
        :z: The z coordinate of the cube.
        :size: The size of the cube.
        """
        X = x + size + 0.01
        Y = y + size + 0.01
        Z = z + size + 0.01
        x = x - 0.01
        y = y - 0.01
        z = z - 0.01
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), ('c4B', (255, 255, 255, 5) * 4))
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v3f', (x, y, z,  X, y, z,  X, y, Z,  x, y, Z)), ('c4B', (255, 255, 255, 5) * 4))
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), ('c4B', (255, 255, 255, 5) * 4))
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)), ('c4B', (255, 255, 255, 5) * 4))
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), ('c4B', (255, 255, 255, 5) * 4))
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v3f', (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)), ('c4B', (255, 255, 255, 5) * 4))

    def draw_player_hitbox(self, pos):
        """
        draw_player_hitbox

        * Draws the player hitbox.

        :pos: The position of the player.
        """
        self.draw_cube(pos[0], pos[1], pos[2], 1)

    def draw(self):
        """
        draw

        * Draws the world.
        """
        # Lights
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_LIGHT7)
        glLightfv(GL_LIGHT7, GL_AMBIENT, (GLfloat * 4)(*self.light_color))
        self._tick += 1
        if self.player.pointing_at[0] != None:
            self.draw_player_hitbox(self.parent.player.pointing_at[0])
        for i in self.chunks:
            chunk = self.chunks[i]
            if chunk is not None and chunk.generated:
                chunk.draw()
        self.cloud_generator.draw()
        self._scheduler.run()
        self._scheduler_.run()

    def make_chunk(self, xz, index):
        """
        make_chunk

        * Makes a chunk.

        :xz: The xz coordinates of the chunk.
        :index: The index of the chunk.
        """
        chunk = Chunk(xz[0], xz[1], self)
        self.chunks[index] = chunk
        chunk.generate()

    def chunk_exists(self, index):
        """
        chunk_exists

        * Checks if a chunk exists.

        :index: The index of the chunk.

        :returns: True if the chunk exists, False if not.
        """
        return index in self.chunks

    def block_exists(self, coords):
        """
        block_exists

        * Checks if a block exists.

        :coords: The coordinates of the block.

        :returns: True if the block exists, False if not.
        """
        try:
            return self._all_blocks[(coords[0], coords[1], coords[2])].block_data
        except:
            return False

    def add_row_z_minus(self):
        """
        add_row_z_minus

        * Adds a row of blocks to the world.
        """
        data = {}
        for x in range(-self.chunk_distance, self.chunk_distance):
            if not self.chunk_exists((self.x+x, self.z-self.chunk_distance)):
                data[(self.x+x, self.z-self.chunk_distance)
                     ] = Chunk(self.x+x, self.z-self.chunk_distance, self)
                self._scheduler_.add_task(
                    data[self.x+x, self.z-self.chunk_distance].generate)
        for i in data:
            self.chunks[i] = data[i]
        self.z -= 1

    def add_row_z_plus(self):
        """
        add_row_z_plus

        * Adds a row of blocks to the world.
        """
        data = {}
        for x in range(-self.chunk_distance, self.chunk_distance):
            if not self.chunk_exists((self.x+x, self.z+self.chunk_distance)):
                data[(self.x+x, self.z+self.chunk_distance)
                     ] = Chunk(self.x+x, self.z+self.chunk_distance, self)
                self._scheduler_.add_task(
                    data[self.x+x, self.z+self.chunk_distance].generate)
        for i in data:
            self.chunks[i] = data[i]
        self.z += 1

    def add_row_x_minus(self):
        """
        add_row_x_minus

        * Adds a row of blocks to the world.
        """
        data = {}
        for z in range(-self.chunk_distance, self.chunk_distance):
            if not self.chunk_exists((self.x-self.chunk_distance, self.z+z)):
                data[(self.x-self.chunk_distance, self.z+z)
                     ] = Chunk(self.x-self.chunk_distance, self.z+z, self)
                self._scheduler_.add_task(
                    data[self.x-self.chunk_distance, self.z+z].generate)
        for i in data:
            self.chunks[i] = data[i]
        self.x -= 1

    def add_row_x_plus(self):
        """
        add_row_x_plus

        * Adds a row of blocks to the world.
        """
        data = {}
        for z in range(-self.chunk_distance, self.chunk_distance):
            if not self.chunk_exists((self.x+self.chunk_distance, self.z+z)):
                data[(self.x+self.chunk_distance, self.z+z)
                     ] = Chunk(self.x+self.chunk_distance, self.z+z, self)
                self._scheduler_.add_task(
                    data[self.x+self.chunk_distance, self.z+z].generate)
        for i in data:
            self.chunks[i] = data[i]
        self.x += 1

    def _check_no_holes(self):
        """
        _check_no_holes

        * Checks if there are any holes in the world.
        """
        for i in range(self.x-self.chunk_distance+1, self.x+self.chunk_distance-1):
            for j in range(self.z-self.chunk_distance+1, self.z+self.chunk_distance-1):
                if not self.chunk_exists((i, j)):
                    self.make_chunk((i, j), (i, j))

    def remove_block(self, coords):
        """
        remove_block

        * Removes a block from the world.
        """
        if self._all_blocks[(coords[0], coords[1], coords[2])].generated:
            self._all_blocks[(coords[0], coords[1], coords[2])].chunk.remove_block(tuple(coords))
            self._all_blocks[(coords[0], coords[1], coords[2])].remove()

    def add_block(self, coords, block_type, parent):
        """
        add_block

        * Adds a block to the world.
        """
        parent.add_block(type_=block_type, block_data={"block_pos":{"x":coords[0], "y":coords[1], "z":coords[2]}}, index=tuple(coords))

    def _do_daynight(self):
        """
        _do_daynight

        * Updates the day/night cycle.
        """
        if self.light_color[0] > self.daynight_max:
            self.light_change = -0.0001
        elif self.light_color[0] < self.daynight_min:
            self.light_change = 0.0001
        self.light_color[0] += self.light_change
        self.light_color[1] += self.light_change
        self.light_color[2] += self.light_change

    def update(self, dt):
        """
        update

        * Updates the world.

        :dt: The time since the last update.
        """
        self._do_daynight()
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
