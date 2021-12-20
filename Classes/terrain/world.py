# imports
import pyglet
from pyglet.gl import *
import os
import random
from tqdm import trange

# Inbuilt imports
from logger import *
import Classes as pycraft

# all the block types
blocks_all = {}

# Function to load a texture
def load_texture(filename):
    """
    load_texture

    * Loads a texture from a file

    :filename: path of the file to load
    """
    try:
        tex = pyglet.image.load(filename).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)
    except:
        warn("Texture Loader", "Failed to load texture: " + filename)
        return None

class World:
    def __init__(self, parent):
        """
        World

        * Initializes the world

        :parent: the parent window
        """
        self.parent = parent
        self.generator = pycraft.TerrainGenerator

        self.textures = {}
        self.block_types = {}
        self.structure_types = {}
        
        self.all_blocks = {}
        self._independent_blocks = {}
        self.all_chunks = {}

        self._load_textures()
        self._load_block_types()
        self._load_structures()

        self.render_distance = 5
        self.chunk_size = 8
        self.infgen_threshold = 0
        self.position = [0, 0]

        self.seed = random.randint(0, 100000)

        self._queue = []
        self.generate()

    def _load_textures(self):
        """
        _load_textures

        * Loads all the textures
        """
        log("Texture Loader", "Loading textures...")
        for i in os.listdir("assets/textures/block"):
            if i.endswith(".png"):
                self.textures[i.split(".")[0]] = load_texture("assets/textures/block"+"/"+i)
        log("Texture Loader", "Loaded " + str(len(self.textures)) + " textures")

    def _load_block_types(self):
        """
        _load_block_types
        
        * Loads all the block types
        """
        log("Block Loader", "Loading blocks...")
        for i in os.listdir("Classes/terrain/blocks"):
            if i.endswith(".py") and i != "__init__.py":
                self.block_types[i.split(".")[0]] = __import__("Classes.terrain.blocks." + i.split(".")[0], fromlist = [i.split(".")[0]]).Block(self)
        log("Block Loader", "Loaded " + str(len(self.block_types)) + " blocks")

    def _load_structures(self):
        """
        _load_structures

        * Loads all the structures
        """
        log("Structure Loader", "Loading structures...")
        self.structure_types = pycraft.load_structures(self)
        log("Structure Loader", "Loaded " + str(len(self.structure_types)) + " structures")

    def generate(self):
        """
        generate

        * Generates the world
        """
        info("World", "Generating world...")
        for i in trange(-self.render_distance+1, self.render_distance):
            for j in range(-self.render_distance+1, self.render_distance):
                self.all_chunks[(i, j)] = pycraft.Chunk(self, {'x': i, 'z': j})
                self._queue.append((i, j))

    def update(self):
        """
        update

        * Updates the world
        """
        # Updates the chunks
        for i in self.all_chunks:
            self.all_chunks[i].update()

        # Runs the queue
        self._process_queue_item()

        # INFGEN
        if self.parent.player.pos[0] / self.chunk_size > self.position[0] + self.infgen_threshold:
            self.add_row_x_plus()
        if self.parent.player.pos[0] / self.chunk_size < self.position[0] - self.infgen_threshold:
            self.add_row_x_minus()
        if self.parent.player.pos[2] / self.chunk_size > self.position[1] + self.infgen_threshold:
            self.add_row_z_plus()
        if self.parent.player.pos[2] / self.chunk_size < self.position[1] - self.infgen_threshold:
            self.add_row_z_minus()

    def draw(self):
        """
        draw

        * Draws the world
        """
        for i in self.all_chunks:
            self.all_chunks[i].draw()
        if self.parent.player.pointing_at[0] != None:
            self.draw_cube(self.parent.player.pointing_at[0][0], self.parent.player.pointing_at[0][1], self.parent.player.pointing_at[0][2], 1)

    def draw_cube(self, x, y, z, size):
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

    def block_exists(self, position):
        """
        block_exists

        * Checks if a block exists at a position

        :position: the position to cdheck
        """
        if position in self.all_blocks:
            return True
        else:
            return False

    def chunk_exists(self, position):
        """
        chunk_exists

        * Checks if a chunk exists at a position

        :position: the position to cdheck
        """
        if position in self.all_chunks:
            return True
        else:
            return False

    def make_chunk(self, position):
        """
        make_chunk

        * Makes a chunk at a position

        :position: the position to make the chunk at
        """
        self.all_chunks[position] = pycraft.Chunk(self, {'x': position[0], 'z': position[1]})
        self._queue.append(position)

    def make_structure(self, position, structure_type, chunk):
        """
        make_structures

        * Makes all the structures at a position

        :position: the position to make the structures at
        """
        chunk.structures[position] = self.structure_types[structure_type](chunk, position)
        chunk.structures[position].generate()

    def _process_queue_item(self):
        """
        _process_queue_item

        * Processes an item in the queue
        """
        if len(self._queue) > 0:
            item = self._queue[0]
            self.all_chunks[item].generate()
            self._queue.pop(0)

    def get_block(self, position):
        """
        get_block

        * Gets a block at a position

        :position: the position to get the block from
        """
        if position in self.all_blocks:
            return self.all_blocks[position]
        else:
            return None
        
    def add_block(self, position, block, chunk):
        """
        add_block

        * Adds a block at a position

        :position: the position to add the block to
        :block: the block to add
        """
        self.all_blocks[position] = block
        chunk.add_block(position, block)

    def remove_block(self, position, chunk):
        """
        remove_block

        * Removes a block at a position

        :position: the position to remove the block from
        """
        if tuple(position) in self.all_blocks:
            chunk.remove_block(position)

    def add_row_x_minus(self):
        """
        add_row_x_minus

        * Adds a row of blocks to the world.
        """
        for z in range(-self.render_distance, self.render_distance):
            if not self.chunk_exists((self.position[0]-self.render_distance, self.position[1]+z)):
                self.make_chunk((self.position[0]-self.render_distance, self.position[1]+z))
        self.position[0] -= 1

    def add_row_x_plus(self):
        """
        add_row_x_plus

        * Adds a row of blocks to the world.
        """
        for z in range(-self.render_distance, self.render_distance):
            if not self.chunk_exists((self.position[0]+self.render_distance, self.position[1]+z)):
                self.make_chunk((self.position[0]+self.render_distance, self.position[1]+z))
        self.position[0] += 1

    def add_row_z_minus(self):
        """
        add_row_z_minus

        * Adds a row of blocks to the world.
        """
        for x in range(-self.render_distance, self.render_distance):
            if not self.chunk_exists((self.position[0]+x, self.position[1]-self.render_distance)):
                self.make_chunk((self.position[0]+x, self.position[1]-self.render_distance))
        self.position[1] -= 1

    def add_row_z_plus(self):
        """
        add_row_z_plus

        * Adds a row of blocks to the world.
        """
        for x in range(-self.render_distance, self.render_distance):
            if not self.chunk_exists((self.position[0]+x, self.position[1]+self.render_distance)):
                self.make_chunk((self.position[0]+x, self.position[1]+self.render_distance))
        self.position[1] += 1
