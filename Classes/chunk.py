from pyglet import gl
from pyglet.gl import *
import pyglet
import random
from opensimplex import OpenSimplex
import threading
import time

simplex = OpenSimplex(seed=random.randint(0, 100000))

def get_tex(file):
        tex = pyglet.image.load(file).texture
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

top = get_tex('assets/grass_top.png')
side = get_tex('assets/grass_side.png')
bottom = get_tex('assets/dirt.png')

class Chunk:
    def __init__(self, X, Z, parent):
        self.parent = parent
        self.X = X
        self.Z = Z
        self.generated = False
    
    def generate(self):
        self.batch = pyglet.graphics.Batch()
        self.CHUNK_DIST = 16

        self.blocks = []
        self.graphics = {}

        self.X = self.X*self.CHUNK_DIST
        self.Z = self.Z*self.CHUNK_DIST

        for x in range(int(self.X), int(self.X+self.CHUNK_DIST)):
            for y in range(int(self.Z), int(self.Z+self.CHUNK_DIST)):
                self.blocks.append(
                    (x, int(simplex.noise2d(x/10, y/10)*5), y))
                self.add_block(x=x-self.X, y=int(
                    simplex.noise2d(x/10, y/10)*5), z=y-self.Z, batch=self.batch)
        self.generated = True

    def add_block(self, x, y, z, batch=None):
        X, Y, Z = x+1, y+1, z+1

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))

        batch.add(4, GL_QUADS, side,   ('v3f', (X, y,
                       z,  x, y, z,  x, Y, z,  X, Y, z)), tex_coords)  # back
        batch.add(4, GL_QUADS, side,   ('v3f', (x, y,
                       Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), tex_coords)  # front

        batch.add(4, GL_QUADS, side,   ('v3f', (x, y,
                       z,  x, y, Z,  x, Y, Z,  x, Y, z)), tex_coords)  # left
        batch.add(4, GL_QUADS, side,   ('v3f', (X, y,
                       Z,  X, y, z,  X, Y, z,  X, Y, Z)), tex_coords)  # right

        batch.add(4, GL_QUADS, bottom, ('v3f', (x, y,
                       z,  X, y, z,  X, y, Z,  x, y, Z)), tex_coords)  # bottom
        batch.add(4, GL_QUADS, top,    ('v3f', (x, Y,
                       Z,  X, Y, Z,  X, Y, z,  x, Y, z)), tex_coords)  # top

    def draw(self):
        if self.generated:
            glPushMatrix()
            glTranslatef(self.X, 0, self.Z)
            self.batch.draw()
            glPopMatrix()
