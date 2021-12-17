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
        
        self.all_blocks = {}
        self.all_chunks = {}

        self._load_textures()
        self._load_block_types()

        self.render_distance = 3
        self.chunk_size = 16

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

    def generate(self):
        """
        generate

        * Generates the world
        """
        info("World", "Generating world...")
        for i in trange(-self.render_distance, self.render_distance):
            for j in range(-self.render_distance, self.render_distance):
                self.all_chunks[(i, j)] = pycraft.Chunk(self, {'x': i, 'z': j})
                self._queue.append((i, j))

    def update(self):
        """
        update

        * Updates the world
        """
        for i in self.all_chunks:
            self.all_chunks[i].update()
        self._process_queue_item()

    def draw(self):
        """
        draw

        * Draws the world
        """
        for i in self.all_chunks:
            self.all_chunks[i].draw()

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

        :position: the position to check
        """
        if position in self.all_blocks:
            _ = position
            return [True, _]
        else:
            return [False, None]

    def _process_queue_item(self):
        """
        _process_queue_item

        * Processes an item in the queue
        """
        if len(self._queue) > 0:
            item = self._queue[0]
            self.all_chunks[item].generate()
            self._queue.pop(0)
