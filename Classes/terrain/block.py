# imports
import pyglet
from pyglet.gl import *
import random

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
        self._preloads = {}

        self.tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))

        self._preload_queue = []
    
    def _preload_block(self, position, parent):
        self.parent.all_blocks[tuple(position)] = [self.name, tuple(position)]
        self._preloads[tuple(position)] = parent
        self._preload_queue.append(parent)

    def add(self, position, parent):
        """
        add

        * Adds a block to the world

        :position: the position of the block
        """
        data = {"faces": {"top": None, "bottom": None, "front": None, "back": None, "left": None, "right": None}, parent: parent}

        x, y, z = position
        X, Y, Z = (x + 1, y + 1, z + 1)
        
        if not parent.parent.block_exists((x, y + 1, z)):
            data["faces"]['top'] = parent.batch.add(4, GL_QUADS, self.texture['top'],    ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), self.tex_coords)

        if not parent.parent.block_exists((x, y - 1, z)):
            data["faces"]['bottom'] = parent.batch.add(4, GL_QUADS, self.texture['bottom'], ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z)), self.tex_coords)

        if not parent.parent.block_exists((x - 1, y, z)):
            data["faces"]['left'] = parent.batch.add(4, GL_QUADS, self.texture['left'],   ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), self.tex_coords)

        if not parent.parent.block_exists((x + 1, y, z)):
            data["faces"]['right'] = parent.batch.add(4, GL_QUADS, self.texture['right'],  ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)), self.tex_coords)

        if not parent.parent.block_exists((x, y, z + 1)):
            data["faces"]['front'] = parent.batch.add(4, GL_QUADS, self.texture['front'],  ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), self.tex_coords)

        if not parent.parent.block_exists((x, y, z - 1)):
            data["faces"]['back'] = parent.batch.add(4, GL_QUADS, self.texture['back'],   ('v3f', (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)), self.tex_coords)

        self.instances[tuple(position)] = data

        returned_data = [self.name, tuple(position)]

        parent.parent.all_blocks[tuple(position)] = returned_data
        return returned_data

    def _process_preloads(self, chunk):
        for _ in list(self._preloads).copy():
            if self._preloads[_] == chunk:
                self.add(position = _, parent = self._preloads[_])

        for i in range(len(self._preload_queue)):
            if self._preload_queue[i] == chunk:
                self._preload_queue.pop(i)
                break

    def remove(self, position):
        """
        remove

        * Removes a block from the world

        :position: the position of the block
        """
        if position in self.instances:
            for i in self.instances[position]["faces"]:
                self.instances[position]["faces"][i].delete()
