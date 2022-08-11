from models.cube import *
from models.slab import *

def add_position(position, vertices):
    vertices = list(vertices)
    for i in range(0, len(vertices), 3):
        vertices[i] += position[0]
        vertices[i+1] += position[1]
        vertices[i+2] += position[2]
    return vertices
