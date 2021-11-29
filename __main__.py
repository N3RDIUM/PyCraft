test = False

from logger import *
from load_shaders import *
from Classes.window import *
from Classes.world import *
from Classes.chunk import *
from Classes.player import *
from pyglet.gl import *
from OpenGL.GL import *
import pyglet


if test:
    warn('Main', "This is a test!")


def use_shader(shader_name="default"):
    log("main", f"Using shaders: {shader_name}:{shaders[shader_name]}")
    glLinkProgram(shaders[shader_name])
    glUseProgram(shaders[shader_name])


use_shaders = False
load_shaders()

if __name__ == '__main__':
    window = Window(width=400, height=300, caption='PyCraft',
                    resizable=True)
    glClearColor(0.5, 0.7, 1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    if not test:
        glEnable(GL_FOG)
        glFogfv(GL_FOG_COLOR, (GLfloat *
                int(window.model.chunk_distance*16))(0.5, 0.69, 1.0, 10))
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogf(GL_FOG_START, window.model.chunk_distance*3)
        glFogf(GL_FOG_END, window.model.chunk_distance*4)
        glEnable (GL_LINE_SMOOTH)
        glEnable (GL_BLEND)
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glHint (GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    # shaders
    if use_shaders:
        use_shader()
    pyglet.app.run()
