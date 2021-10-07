from pyglet import gl
from pyglet.gl import *
import pyglet
import random
from opensimplex import OpenSimplex

simplex = OpenSimplex(seed=random.randint(0, 100000))

class Chunk:
    def __init__(self,X,Y,Z):
        self.top = self.get_tex('assets/grass_top.png')
        self.side = self.get_tex('assets/grass_side.png')
        self.bottom = self.get_tex('assets/dirt.png')

        self.batch = pyglet.graphics.Batch()
        self.CHUNK_DIST = 16

        self.blocks = []
        self.graphics = {}

        self.X = X*self.CHUNK_DIST
        self.Y = Y*self.CHUNK_DIST
        self.Z = Z*self.CHUNK_DIST

        for x in range(-int(self.CHUNK_DIST/2),int(self.CHUNK_DIST/2)):
            for y in range(-int(self.CHUNK_DIST/2),int(self.CHUNK_DIST/2)):
                    self.blocks.append((x,int(simplex.noise2d(x/10,y/10)*5),y))
                    self.add_block(x,int(simplex.noise2d(x/10,y/10)*5),y)

        self.blocks = random.sample(self.blocks,len(self.blocks))

    def get_tex(self,file):
        tex = pyglet.image.load(file).texture
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)

    def add_block(self,x,y,z):
        X, Y, Z = x+1, y+1, z+1

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))

        self.batch.add(4, GL_QUADS, self.side,   ('v3f', (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)), tex_coords) # back
        self.batch.add(4, GL_QUADS, self.side,   ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), tex_coords) # front

        self.batch.add(4, GL_QUADS, self.side,   ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), tex_coords)  # left
        self.batch.add(4, GL_QUADS, self.side,   ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)), tex_coords)  # right

        self.batch.add(4, GL_QUADS, self.bottom, ('v3f', (x, y, z,  X, y, z,  X, y, Z,  x, y, Z)), tex_coords)  # bottom
        self.batch.add(4, GL_QUADS, self.top,    ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), tex_coords)  # top

    def draw(self):
        glPushMatrix()
        glTranslatef(self.X, self.Y, self.Z)
        self.batch.draw()
        glPopMatrix()
