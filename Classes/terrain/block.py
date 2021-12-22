# imports
import pyglet
from pyglet.gl import *
import random

class Block:
    """
    Block

    * Base block class
    """
    def __init__(self, name, parent):
        """
        Block.__init__

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
        """
        _preload_block

        * Preloads a block

        :position: the position of the block
        :parent: the parent window
        """
        self.parent.all_blocks[tuple(position)] = [self.name, tuple(position)]
        self._preloads[tuple(position)] = parent
        self._preload_queue.append(parent)

    def add(self, position, parent):
        """
        add

        * Adds a block to the world

        :position: the position of the block
        """
        data = {"faces": {"top": None, "bottom": None, "front": None, "back": None, "left": None, "right": None}, "parent": parent}

        x, y, z = position
        X, Y, Z = (x + 1, y + 1, z + 1)
        
        if not parent.parent.block_exists((x, y + 1, z)):
            data["faces"]['top'] = self.parent.batch.add(4, GL_QUADS, self.texture['top'],    ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), self.tex_coords)

        if not parent.parent.block_exists((x, y - 1, z)):
            data["faces"]['bottom'] = self.parent.batch.add(4, GL_QUADS, self.texture['bottom'], ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z)), self.tex_coords)

        if not parent.parent.block_exists((x - 1, y, z)):
            data["faces"]['left'] = self.parent.batch.add(4, GL_QUADS, self.texture['left'],   ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), self.tex_coords)

        if not parent.parent.block_exists((x + 1, y, z)):
            data["faces"]['right'] = self.parent.batch.add(4, GL_QUADS, self.texture['right'],  ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)), self.tex_coords)

        if not parent.parent.block_exists((x, y, z + 1)):
            data["faces"]['front'] = self.parent.batch.add(4, GL_QUADS, self.texture['front'],  ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), self.tex_coords)

        if not parent.parent.block_exists((x, y, z - 1)):
            data["faces"]['back'] = self.parent.batch.add(4, GL_QUADS, self.texture['back'],   ('v3f', (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)), self.tex_coords)

        self.instances[tuple(position)] = data

        returned_data = [self.name, tuple(position), lambda: self._update_faces(tuple(position))]

        parent.parent.all_blocks[tuple(position)] = returned_data
        return returned_data

    def _update_faces(self, position):
        """
        _update_faces

        * Updates the faces of a block

        :position: the position of the block
        """
        try:
            _parent = self.instances[position]["parent"]
            self._remove(position)
            self.add(position, _parent)
        except KeyError:
            pass

    def _process_preloads(self, chunk):
        """
        _process_preloads

        * Processes the preloads

        :chunk: the chunk to process
        """
        for _ in list(self._preloads).copy():
            if self._preloads[_] == chunk:
                self.add(position = _, parent = self._preloads[_])

        for i in range(len(self._preload_queue)):
            if self._preload_queue[i] == chunk:
                self._preload_queue.pop(i)
                break

    def _remove(self, position):
        try:
            if self.instances[position]["faces"]["top"] is not None:
                self.instances[position]["faces"]["top"].delete()

            if self.instances[position]["faces"]["bottom"] is not None:
                self.instances[position]["faces"]["bottom"].delete()

            if self.instances[position]["faces"]["front"] is not None:
                self.instances[position]["faces"]["front"].delete()

            if self.instances[position]["faces"]["back"] is not None:
                self.instances[position]["faces"]["back"].delete()

            if self.instances[position]["faces"]["left"] is not None:
                self.instances[position]["faces"]["left"].delete()

            if self.instances[position]["faces"]["right"] is not None:
                self.instances[position]["faces"]["right"].delete()
        except KeyError:
            pass

    def remove(self, position):
        """
        remove

        * Removes a block from the world

        :position: the position of the block
        """
        self._remove(position)

        x = position[0]
        y = position[1]
        z = position[2]
        
        try:
            del self.instances[position]
            del self.parent.all_blocks[position]
        except KeyError:
            pass

        if (x, y + 1, z) in self.parent.all_blocks:
            self.parent.all_blocks[(x, y + 1, z)][2]()

        if (x, y - 1, z) in self.parent.all_blocks:
            self.parent.all_blocks[(x, y - 1, z)][2]()

        if (x - 1, y, z) in self.parent.all_blocks:
            self.parent.all_blocks[(x - 1, y, z)][2]()

        if (x + 1, y, z) in self.parent.all_blocks:
            self.parent.all_blocks[(x + 1, y, z)][2]()

        if (x, y, z + 1) in self.parent.all_blocks:
            self.parent.all_blocks[(x, y, z + 1)][2]()

        if (x, y, z - 1) in self.parent.all_blocks:
            self.parent.all_blocks[(x, y, z - 1)][2]()
