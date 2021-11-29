from pyglet.gl import *
from opensimplex import OpenSimplex
import random

seed = random.randint(-999999, 999999)
noise = OpenSimplex(seed=seed)


class cloud:
    def __init__(self, x, z):
        self.pos = [x, z]
        self.size = [10, 10]

    def draw(self):
        x = self.pos[0]
        y = 50
        z = self.pos[1]

        X = x+self.size[0]
        Y = y+10
        Z = z+self.size[1]

        glPushMatrix()
        glColor3f(0.8, 0.8, 0.8)
        pyglet.graphics.draw(4, pyglet.gl.GL_QUADS,
                             ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)))
        glColor3f(1, 1, 1)
        glPopMatrix()
