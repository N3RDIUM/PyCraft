# imports
from Classes import *
from opensimplex import OpenSimplex
import random
from pyglet.gl import *

# Cloud Generator
class CloudGenerator:
    def __init__(self, parent):
        """
        CloudGenerator

        *This is a cloud generator for the world.

        :parent: the parent world
        """
        self.clouds = []
        self.frame = 0
        self.seed = random.randint(-999999, 999999)
        self.noise = OpenSimplex(self.seed)
        self.parent = parent
        self.trans_z = 0

    def draw(self):
        self.frame += 1
        self.trans_z += 0.1

        glPushMatrix()
        glTranslatef(self.parent.player.pos[0], 0, self.parent.player.pos[1])
        for i in self.clouds:
            self.clouds[i].draw()
        glPopMatrix()

        self.generate_for_frame()

    def generate_for_frame(self):
        """
        Generates clouds for the current frame

        returns: None
        """
        distance = self.parent.CHUNK_DIST * self.parent.chunk_distance
        noise_val = self.noise.noise2d(self.frame/100, self.trans_z/100)*10
