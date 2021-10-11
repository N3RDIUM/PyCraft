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

class PrepareBatch(threading.Thread):
    def __init__(self, chunk, XYZ):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.chunk = chunk
        self.xyz = XYZ
        self.start()

    def start(self):
        threading.Thread.start(self)
        x = self.xyz[0]
        y = self.xyz[1]
        z = self.xyz[2]
        X, Y, Z = x+1, y+1, z+1

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))

        self.chunk.batch.add(4, GL_QUADS, side,   ('v3f', (X, y,
                       z,  x, y, z,  x, Y, z,  X, Y, z)), tex_coords)  # back
        self.chunk.batch.add(4, GL_QUADS, side,   ('v3f', (x, y,
                       Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), tex_coords)  # front

        self.chunk.batch.add(4, GL_QUADS, side,   ('v3f', (x, y,
                       z,  x, y, Z,  x, Y, Z,  x, Y, z)), tex_coords)  # left
        self.chunk.batch.add(4, GL_QUADS, side,   ('v3f', (X, y,
                       Z,  X, y, z,  X, Y, z,  X, Y, Z)), tex_coords)  # right

        self.chunk.batch.add(4, GL_QUADS, bottom, ('v3f', (x, y,
                       z,  X, y, z,  X, y, Z,  x, y, Z)), tex_coords)  # bottom
        self.chunk.batch.add(4, GL_QUADS, top,    ('v3f', (x, Y,
                       Z,  X, Y, Z,  X, Y, z,  x, Y, z)), tex_coords)  # top


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
                PrepareBatch(self,(x-self.X, int(
                    simplex.noise2d(x/10, y/10)*5), y-self.Z))
        self.generated = True
        
    def draw(self):
        if self.generated:
            glPushMatrix()
            glTranslatef(self.X, 0, self.Z)
            self.batch.draw()
            glPopMatrix()
