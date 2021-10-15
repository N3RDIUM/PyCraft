import pyglet
from pyglet.window import key
from pyglet.gl import *
from Classes.player import *
from Classes.chunk import *
from Classes.world import *
from Classes.window import *

def player(dt): 
    window.player.pos[2] -= 0.1
    window.player.pos[1]  = 10

if __name__ == '__main__':
    window = Window(width=400, height=300, caption='PyCraft',
                    resizable=True, Chunk=Chunk, Player=Player, World=World)
    glClearColor(0.5, 0.7, 1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, (GLfloat * int(window.model.chunk_distance*100))(0.5, 0.69, 1.0, 1))
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, window.model.chunk_distance/1600)
    glFogf(GL_FOG_END, window.model.chunk_distance*16)
    pyglet.clock.schedule(player)
    pyglet.app.run()