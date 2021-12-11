# imports
from pyglet.window.key import I
from Classes.environment.environment_objects import *
from opensimplex import OpenSimplex
import random
from pyglet.gl import *
from pyglet.graphics import Batch

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
        self.trans_z += 0.05

        for cloud in self.clouds:
            cloud.draw()

        if self.frame % 2 == 0:
            self.generate_for_frame()

    def generate_for_frame(self):
        """
        Generates clouds for the current frame

        returns: None
        """
        self.clouds = []

        for i in range(self.parent.x-self.parent.chunk_distance, self.parent.x+self.parent.chunk_distance):
            for j in range(self.parent.z-self.parent.chunk_distance, self.parent.z+self.parent.chunk_distance):
                if abs(self.noise.noise2d(i, j))*2 > 0.7:
                    self.clouds.append(Cloud((i*4, j*4), self))
