import pyglet
from pyglet.window import key
from pyglet.gl import *
from Classes.player import *
from Classes.chunk import *
from Classes.window import *

if __name__ == '__main__':
    window = Window(width=400, height=300, caption='PyCraft', resizable=True, Chunk=Chunk, Player=Player)
    glClearColor(0.5, 0.7, 1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    pyglet.app.run()
