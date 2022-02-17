#################################################################
#  ______   __  __   ______   ______     __     ______   ______ *
# |  __  |  \ \/ /  |  ____| |  __  |   /__\   /  ____| |__  __|*
# | |__| |   \  /   | |      | |__| |  //__\\ | |__       |  |  *
# |  ____|    ||    | |      |______| / ____ \|  __|      |  |  *
# | |         ||    | |____  | |\ \  / /    \ | |         |  |  *
# |_|         ||    |______| |_| \_\/_/      \|_|         |__|  *
#################################################################

# imports
import random
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

for i in range(-10, 10):
    for j in range(-10, 10):
        x = i
        y = random.randint(-1, 1)
        z = j
        renderer.add_cube((x, y, z))

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

def update_on_resize():
    _setup_3d()
    glViewport(0, 0, *get_window_size())

# mainloop
while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    update_on_resize()

    _setup_3d()
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glColor3f(1.0, 1.0, 1.0)

    # First person camera translation and rotation
    glRotatef(camrot[0], 1, 0, 0)
    glRotatef(camrot[1], 0, 1, 0)
    glTranslatef(-campos[0], -campos[1], -campos[2])

    # keyboard input
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    # wasd movement
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        campos[2] -= 0.1
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        campos[2] += 0.1
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        campos[0] -= 0.1
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        campos[0] += 0.1
    # Space and shift
    if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
        campos[1] += 0.1
    if glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
        campos[1] -= 0.1
    # Arrow keys rotation
    if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
        camrot[0] -= 1
    if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
        camrot[0] += 1
    if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
        camrot[1] -= 1
    if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
        camrot[1] += 1

    renderer.render()

    glfw.poll_events()
    glfw.swap_buffers(window)

glfw.terminate()
