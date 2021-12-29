# imports
from pyglet.gl import *

class Liquid:
    def __init__(self, name, parent):
        self.name = name
        self.texture_still = None
        self.texture_flow = None
        self.list_single_row = (
            ('t2f', (0, 0,  1, 0,  1, 1/30,  0, 1/30)),
            ('t2f', (0, 1/30,  1, 1/30,  1, 2/30,  0, 2/30)),
            ('t2f', (0, 2/30,  1, 2/30,  1, 3/30,  0, 3/30)),
            ('t2f', (0, 3/30,  1, 3/30,  1, 4/30,  0, 4/30)),
            ('t2f', (0, 4/30,  1, 4/30,  1, 5/30,  0, 5/30)),
            ('t2f', (0, 5/30,  1, 5/30,  1, 6/30,  0, 6/30)),
            ('t2f', (0, 6/30,  1, 6/30,  1, 7/30,  0, 7/30)),
            ('t2f', (0, 7/30,  1, 7/30,  1, 8/30,  0, 8/30)),
            ('t2f', (0, 8/30,  1, 8/30,  1, 9/30,  0, 9/30)),
            ('t2f', (0, 9/30,  1, 9/30,  1, 10/30,  0, 10/30)),
            ('t2f', (0, 10/30,  1, 10/30,  1, 11/30,  0, 11/30)),
            ('t2f', (0, 11/30,  1, 11/30,  1, 12/30,  0, 12/30)),
            ('t2f', (0, 12/30,  1, 12/30,  1, 13/30,  0, 13/30)),
            ('t2f', (0, 13/30,  1, 13/30,  1, 14/30,  0, 14/30)),
            ('t2f', (0, 14/30,  1, 14/30,  1, 15/30,  0, 15/30)),
            ('t2f', (0, 15/30,  1, 15/30,  1, 16/30,  0, 16/30)),
            ('t2f', (0, 16/30,  1, 16/30,  1, 17/30,  0, 17/30)),
            ('t2f', (0, 17/30,  1, 17/30,  1, 18/30,  0, 18/30)),
            ('t2f', (0, 18/30,  1, 18/30,  1, 19/30,  0, 19/30)),
            ('t2f', (0, 19/30,  1, 19/30,  1, 20/30,  0, 20/30)),
            ('t2f', (0, 20/30,  1, 20/30,  1, 21/30,  0, 21/30)),
            ('t2f', (0, 21/30,  1, 21/30,  1, 22/30,  0, 22/30)),
            ('t2f', (0, 22/30,  1, 22/30,  1, 23/30,  0, 23/30)),
            ('t2f', (0, 23/30,  1, 23/30,  1, 24/30,  0, 24/30)),
            ('t2f', (0, 24/30,  1, 24/30,  1, 25/30,  0, 25/30)),
            ('t2f', (0, 25/30,  1, 25/30,  1, 26/30,  0, 26/30)),
            ('t2f', (0, 26/30,  1, 26/30,  1, 27/30,  0, 27/30)),
            ('t2f', (0, 27/30,  1, 27/30,  1, 28/30,  0, 28/30)),
            ('t2f', (0, 28/30,  1, 28/30,  1, 29/30,  0, 29/30)),
            ('t2f', (0, 29/30,  1, 29/30,  1, 30/30,  0, 30/30)),
        )
        """
        self.list_double_row = (
            ('t2f', (0, 0,  1, 0,  1, 1,  0, 1)),
            ('t2f', (1, 1,  2, 1,  2, 2,  1, 2)),
            ('t2f', (0, 1,  1, 1,  1, 2,  0, 2)),
            ('t2f', (1, 1,  2, 1,  2, 2,  1, 2)),
            ('t2f', (0, 2,  1, 2,  1, 3,  0, 3)),
            ('t2f', (1, 2,  2, 2,  2, 3,  1, 3)),
            ('t2f', (0, 3,  1, 3,  1, 4,  0, 4)),
            ('t2f', (1, 3,  2, 3,  2, 4,  1, 4)),
            ('t2f', (0, 4,  1, 4,  1, 5,  0, 5)),
            ('t2f', (1, 4,  2, 4,  2, 5,  1, 5)),
            ('t2f', (0, 5,  1, 5,  1, 6,  0, 6)),
            ('t2f', (1, 5,  2, 5,  2, 6,  1, 6)),
            ('t2f', (0, 6,  1, 6,  1, 7,  0, 7)),
            ('t2f', (1, 6,  2, 6,  2, 7,  1, 7)),
            ('t2f', (0, 7,  1, 7,  1, 8,  0, 8)),
            ('t2f', (1, 7,  2, 7,  2, 8,  1, 8)),
            ('t2f', (0, 8,  1, 8,  1, 9,  0, 9)),
            ('t2f', (1, 8,  2, 8,  2, 9,  1, 9)),
            ('t2f', (0, 9,  1, 9,  1, 10, 0, 10)),
            ('t2f', (1, 9,  2, 9,  2, 10, 1, 10)),
            ('t2f', (0, 10, 1, 10, 1, 11, 0, 11)),
            ('t2f', (1, 10, 2, 10, 2, 11, 1, 11)),
            ('t2f', (0, 11, 1, 11, 1, 12, 0, 12)),
            ('t2f', (1, 11, 2, 11, 2, 12, 1, 12)),
            ('t2f', (0, 12, 1, 12, 1, 13, 0, 13)),
            ('t2f', (1, 12, 2, 12, 2, 13, 1, 13)),
            ('t2f', (0, 13, 1, 13, 1, 14, 0, 14)),
            ('t2f', (1, 13, 2, 13, 2, 14, 1, 14)),
            ('t2f', (0, 14, 1, 14, 1, 15, 0, 15)),
            ('t2f', (1, 14, 2, 14, 2, 15, 1, 15)),
            ('t2f', (0, 15, 1, 15, 1, 16, 0, 16)),
            ('t2f', (1, 15, 2, 15, 2, 16, 1, 16)),
            ('t2f', (0, 16, 1, 16, 1, 17, 0, 17)),
            ('t2f', (1, 16, 2, 16, 2, 17, 1, 17)),
            ('t2f', (0, 17, 1, 17, 1, 18, 0, 18)),
            ('t2f', (1, 17, 2, 17, 2, 18, 1, 18)),
            ('t2f', (0, 18, 1, 18, 1, 19, 0, 19)),
            ('t2f', (1, 18, 2, 18, 2, 19, 1, 19)),
            ('t2f', (0, 19, 1, 19, 1, 20, 0, 20)),
            ('t2f', (1, 19, 2, 19, 2, 20, 1, 20)),
            ('t2f', (0, 20, 1, 20, 1, 21, 0, 21)),
            ('t2f', (1, 20, 2, 20, 2, 21, 1, 21)),
            ('t2f', (0, 21, 1, 21, 1, 22, 0, 22)),
            ('t2f', (1, 21, 2, 21, 2, 22, 1, 22)),
            ('t2f', (0, 22, 1, 22, 1, 23, 0, 23)),
            ('t2f', (1, 22, 2, 22, 2, 23, 1, 23)),
            ('t2f', (0, 23, 1, 23, 1, 24, 0, 24)),
            ('t2f', (1, 23, 2, 23, 2, 24, 1, 24)),
            ('t2f', (0, 24, 1, 24, 1, 25, 0, 25)),
            ('t2f', (1, 24, 2, 24, 2, 25, 1, 25)),
            ('t2f', (0, 25, 1, 25, 1, 26, 0, 26)),
            ('t2f', (1, 25, 2, 25, 2, 26, 1, 26)),
            ('t2f', (0, 26, 1, 26, 1, 27, 0, 27)),
            ('t2f', (1, 26, 2, 26, 2, 27, 1, 27)),
            ('t2f', (0, 27, 1, 27, 1, 28, 0, 28)),
            ('t2f', (1, 27, 2, 27, 2, 28, 1, 28)),
            ('t2f', (0, 28, 1, 28, 1, 29, 0, 29)),
            ('t2f', (1, 28, 2, 28, 2, 29, 1, 29)),
            ('t2f', (0, 29, 1, 29, 1, 30, 0, 30)),
            ('t2f', (1, 29, 2, 29, 2, 30, 1, 30)),
        )
        """
        self.parent = parent

        self.instances = {}
        self._preload_instances = {}
        self.batch_data = {}

        self.current_index = 0
        self.single_or_double = "single"

    def add_preloaded_instance(self, position):
        """
        Add a preloaded instance to the batch.

        :param position: The position of the instance.
        :type position: tuple
        """
        self._preload_instances[position] = position

    def _process_preloads(self):
        """
        Process the preloaded instances.
        """
        try:
            for position in self._preload_instances:
                self.add(position)
                self._preload_instances.pop(position)
        except:
            pass
        

    def add(self, position):
        x, y, z = position
        X, Y, Z = (x + 1, y + 1, z + 1)

        self.instances[tuple(position)] = [self.name, tuple(position), 0] # Third element is the texture coordinate index
        self.parent.all_liquids[tuple(position)] = self.instances[tuple(position)]
        
        data = {}

        if self.single_or_double == "single":
            data["top"] = self.parent.batch.add(4, GL_QUADS, self.texture_still, ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), self.list_single_row[self.current_index]) if not self.parent.liquid_exists((x, Y, z)) else None
            data["bottom"] = self.parent.batch.add(4, GL_QUADS, self.texture_still, ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z)), self.list_single_row[self.current_index]) if not self.parent.liquid_exists((x, y - 1, z)) else None
            data["left"] = self.parent.batch.add(4, GL_QUADS, self.texture_still, ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), self.list_single_row[self.current_index]) if not self.parent.liquid_exists((x - 1, y, z)) else None
            data["right"] = self.parent.batch.add(4, GL_QUADS, self.texture_still, ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)), self.list_single_row[self.current_index]) if not self.parent.liquid_exists((X, y, z)) else None
            data["front"] = self.parent.batch.add(4, GL_QUADS, self.texture_still, ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), self.list_single_row[self.current_index]) if not self.parent.liquid_exists((x, y, Z)) else None
            data["back"] = self.parent.batch.add(4, GL_QUADS, self.texture_still, ('v3f', (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)), self.list_single_row[self.current_index]) if not self.parent.liquid_exists((x, y, z - 1)) else None

        self.batch_data[tuple(position)] = data

    def update(self):
        try:
            if self.single_or_double == "single":
                self.current_index += 1
                if self.current_index >= len(self.list_single_row):
                    self.current_index = 0
            elif self.single_or_double == "double":
                self.current_index += 1
                if self.current_index >= len(self.list_double_row):
                    self.current_index = 0
            for i in self.instances:
                self._update_faces(i)
            self.flow()
        except RuntimeError:
            pass

    def _update_faces(self, position):
        try:
            for i in self.batch_data[position]:
                if self.batch_data[position][i] != None:
                    self.batch_data[position][i].delete()
            del self.batch_data[tuple(position)]
            self.parent.all_liquids[tuple(position)] = None
            self.add(position)
        except KeyError:
            pass

    def flow(self):
        for i in self.instances:
            if not self.parent.liquid_exists((i[0], i[1], i[2] + 1)) and not self.parent.block_exists((i[0], i[1], i[2] + 1)):
                self.add((i[0], i[1], i[2] + 1))
            if not self.parent.liquid_exists((i[0], i[1], i[2] - 1)) and not self.parent.block_exists((i[0], i[1], i[2] - 1)):
                self.add((i[0], i[1], i[2] - 1))
            if not self.parent.liquid_exists((i[0] + 1, i[1], i[2])) and not self.parent.block_exists((i[0] + 1, i[1], i[2])):
                self.add((i[0] + 1, i[1], i[2]))
            if not self.parent.liquid_exists((i[0] - 1, i[1], i[2])) and not self.parent.block_exists((i[0] - 1, i[1], i[2])):
                self.add((i[0] - 1, i[1], i[2]))
            if not self.parent.liquid_exists((i[0], i[1] - 1, i[2])) and not self.parent.block_exists((i[0], i[1] - 1, i[2])):
                self.add((i[0], i[1] - 1, i[2]))
