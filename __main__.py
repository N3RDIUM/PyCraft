#################################################################
#  ______   __  __   ______   ______     __     ______   ______ *
# |  __  |  \ \/ /  |  ____| |  __  |   /__\   /  ____| |__  __|*
# | |__| |   \  /   | |      | |__| |  //__\\ | |__       |  |  *
# |  ____|    ||    | |      |______| / ____ \|  __|      |  |  *
# | |         ||    | |____  | |\ \  / /    \ | |         |  |  *
# |_|         ||    |______| |_| \_\/_/      \|_|         |__|  *
#################################################################

# imports
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# internal imports
from core.renderer import *
from terrain import *
from player import *

if not glfw.init():
    raise Exception("glfw can not be initialized!")

window = glfw.create_window(800, 500, "PyCraft", None, None)
glfw.make_context_current(window)
renderer = TerrainRenderer(window)
player = Player(window)

glEnable (GL_LINE_SMOOTH)
glEnable(GL_DEPTH_TEST)
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)

renderer.texture_manager.add_from_folder("assets/textures/block/")
renderer.texture_manager.save("atlas.png")
renderer.texture_manager.bind()

world = World(renderer, player)
world.generate()

glEnable(GL_FOG)
glFogfv(GL_FOG_COLOR, (GLfloat *
        int(world.render_distance*16))(0.5, 0.69, 1.0, 10))
glFogfv(GL_FOG_COLOR, (GLfloat * int(world.render_distance*16))(0.5, 0.69, 1.0, 10))
glHint(GL_FOG_HINT, GL_DONT_CARE)
glFogi(GL_FOG_MODE, GL_LINEAR)
glFogf(GL_FOG_START, world.render_distance*3)
glFogf(GL_FOG_END, world.render_distance*4)
glFogf(GL_FOG_START, world.render_distance*4)
glFogf(GL_FOG_END, world.render_distance*5)

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
    glClearColor(0.5, 0.7, 1, 1.0)

    player.update()
    player._translate()
    world.render()

    glfw.poll_events()
    glfw.swap_buffers(window)

glfw.terminate()
