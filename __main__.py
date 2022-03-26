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

    return (
        # top
        x, Y, z,
        x, Y, Z,
        X, Y, Z,
        X, Y, z,

        # bottom
        x, y, z,
        X, y, z,
        X, y, Z,
        x, y, Z,

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
    )

renderer.texture_manager.add_from_folder("assets/textures/block/")
renderer.texture_manager.save("atlas.png")
renderer.texture_manager.bind()

for i in range(-10, 10):
    for j in range(-10, 10):
        x = i
        y = random.randint(-3, 3)
        z = j
        renderer.add(generate_faces([x, y, z]), (
            *renderer.texture_manager.texture_coords["base.png"],
            *renderer.texture_manager.texture_coords["grass.png"],
            *renderer.texture_manager.texture_coords["grass_side.png"],
            *renderer.texture_manager.texture_coords["dirt.png"],
            *renderer.texture_manager.texture_coords["stone.png"],
            *renderer.texture_manager.texture_coords["wood_planks.png"],
        ))

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
