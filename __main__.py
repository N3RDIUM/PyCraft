#################################################################
#  ______   __  __   ______   ______     __     ______   ______ *
# |  __  |  \ \/ /  |  ____| |  __  |   /__\   /  ____| |__  __|*
# | |__| |   \  /   | |      | |__| |  //__\\ | |__       |  |  *
# |  ____|    ||    | |      |______| / ____ \|  __|      |  |  *
# | |         ||    | |____  | |\ \  / /    \ | |         |  |  *
# |_|         ||    |______| |_| \_\/_/      \|_|         |__|  *
#################################################################

# imports
from calendar import c
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# internal imports
from renderer import *

if not glfw.init():
    raise Exception("glfw can not be initialized!")

window = glfw.create_window(800, 500, "PyCraft", None, None)
glfw.make_context_current(window)
renderer = TerrainRenderer(window)

glEnable(GL_DEPTH_TEST)

renderer.add_cube((0, 0, -5))

camrot = [0, 0]
campos = [0, 0, 0]

# get window size
def get_window_size():
    width, height = glfw.get_window_size(window)
    return width, height

def _setup_3d():
    w, h = get_window_size()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(70, w / h, 0.1, 1000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# mainloop
while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    _setup_3d()
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glColor3f(1.0, 1.0, 1.0)
    glTranslatef(0, 0, -10)

    glRotatef(camrot[0], 1, 0, 0)
    glRotatef(camrot[1], 0, 0, 1)
    glTranslatef(-campos[0], -campos[1], -campos[2])

    renderer.render()

    glfw.poll_events()
    glfw.swap_buffers(window)

glfw.terminate()
