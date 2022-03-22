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
from player import *

if not glfw.init():
    raise Exception("glfw can not be initialized!")

window = glfw.create_window(800, 500, "PyCraft", None, None)
glfw.make_context_current(window)
renderer = TerrainRenderer(window)
player = Player(window)

glEnable(GL_DEPTH_TEST)


# generate cube faces
def generate_faces(position):
    x, y, z = position
    X, Y, Z = x + 1, y + 1, z + 1

    return [
        # top
        x, y, z,
        x, y, Z,
        X, y, Z,
        X, y, z,

        # bottom
        x, Y, z,
        X, Y, z,
        X, Y, Z,
        x, Y, Z,

        # left
        x, y, z,
        x, Y, z,
        x, Y, Z,
        x, y, Z,

        # right
        X, y, z,
        X, y, Z,
        X, Y, Z,
        X, Y, z,

        # front
        x, y, z,
        x, Y, z,
        X, Y, z,
        X, y, z,

        # back
        x, y, Z,
        X, y, Z,
        X, Y, Z,
        x, Y, Z,
    ]

defaultTexCoords = [
    # top
    0, 0,
    0, 1,
    1, 1,
    1, 0,

    # bottom
    0, 0,
    1, 0,
    1, 1,
    0, 1,

    # left
    0, 0,
    0, 1,
    1, 1,
    1, 0,

    # right
    0, 0,
    1, 0,
    1, 1,
    0, 1,

    # front
    0, 0,
    0, 1,
    1, 1,
    1, 0,

    # back
    0, 0,
    1, 0,
    1, 1,
    0, 1,
]

for i in range(-10, 10):
    for j in range(-10, 10):
        x = i
        y = random.randint(-1, 1)
        z = j
        renderer.add(generate_faces([x, y, z]), defaultTexCoords)

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

    player.update()
    player._translate()
    renderer.render()

    glfw.poll_events()
    glfw.swap_buffers(window)

glfw.terminate()
