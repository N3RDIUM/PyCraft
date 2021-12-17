# imports
import pyglet
from pyglet.gl import *

class Block:
    def __init__(self, name, parent):
        """
        Block

        * Initializes a block

        :name: name of the block
        :texture: texture of the block
        :parent: the parent window
        """
        self.name = name
        self.texture = {}
        self.parent = parent
        self.instances = {}

        self.tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))

    def add(self, position, parent):
        """
        add

        * Adds a block to the world

        :position: the position of the block
        """
        data = {"faces": {"top": None, "bottom": None, "front": None, "back": None, "left": None, "right": None}, parent: parent}

        x, y, z = position
        X, Y, Z = (x + 1, y + 1, z + 1)
        
        # Top
        if not self.parent.block_exists((x, y - 1, z))[0]:
            data["faces"]["top"] = parent.batch.add(4, GL_QUADS, self.texture["top"], ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), self.tex_coords)
        
        # Bottom
        if self.parent.block_exists((x, y + 1, z))[0]:
            data["faces"]["bottom"] = parent.batch.add(4, GL_QUADS, self.texture["bottom"], ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z)), self.tex_coords)

        # Front
        if not self.parent.block_exists((x, y, z - 1))[0]:
            data["faces"]["front"] = parent.batch.add(4, GL_QUADS, self.texture["front"], ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), self.tex_coords)

        # Back
        if not self.parent.block_exists((x, y, z + 1))[0]:
            data["faces"]["back"] = parent.batch.add(4, GL_QUADS, self.texture["back"], ('v3f', (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)), self.tex_coords)

        # Left
        if not self.parent.block_exists((x-1, y, z))[0]:
            data["faces"]["left"] = parent.batch.add(4, GL_QUADS, self.texture["left"], ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), self.tex_coords)

        # Right
        if not self.parent.block_exists((x+1, y, z))[0]:
            data["faces"]["right"] = parent.batch.add(4, GL_QUADS, self.texture["right"], ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)), self.tex_coords)

        self.instances[tuple(position)] = data

        returned_data = [self.name, tuple(position)]

        parent.parent.all_blocks[tuple(position)] = returned_data
        return returned_data

    def remove(self, position):
        """
        remove

        * Removes a block from the world

        :position: the position of the block
        """
        self.instances[position]

        for i in self.instances[position]["faces"]:
            self.instances[position]["faces"][i].delete()
