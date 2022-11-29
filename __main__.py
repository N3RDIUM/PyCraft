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
import shutil
from OpenGL.GL import *
from OpenGL.GLU import *
from core.logger import *
import subprocess
import multiprocessing
import psutil
import sys

# internal imports
from core.renderer import *
from player import *
from constants import *
from terrain.world import *

# start helpers
try:
    shutil.rmtree("cache/")
except FileNotFoundError:
    pass

if DEV_MODE:
    warn("PyCraaft", "DEV_MODE is enabled. Please don't use this in production.")

chunk_generators = []
chunk_builders   = []

for i in range(psutil.cpu_count()//4):
    chunk_generator =  subprocess.Popen([sys.executable, "helpers/chunk_generator.py"])
    chunk_generators.append(chunk_generator)
    chunk_builder   =  subprocess.Popen([sys.executable, "helpers/chunk_builder.py"])
    chunk_builders.append(chunk_builder)

if not glfw.init():
    raise Exception("glfw can not be initialized!")

if __name__ == "__main__":
    window = glfw.create_window(800, 500, "PyCraft", None, None)
    glfw.make_context_current(window)
    renderer = TerrainRenderer(window)

    renderer.texture_manager.add_from_folder("assets/textures/block/")
    renderer.texture_manager.save("atlas.png")
    renderer.texture_manager.bind()

    world = World(renderer)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    if not DEV_MODE and not USING_RENDERDOC:
        glEnable(GL_FOG)
        glFogfv(GL_FOG_COLOR, (GLfloat * int(32))(0.5, 0.69, 1.0, 10))
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogf(GL_FOG_START, CHUNK_SIZE//2)
        glFogf(GL_FOG_END, (world.render_distance) * CHUNK_SIZE//2 + 1)

    # get window size
    def get_window_size():
        width, height = glfw.get_window_size(window)
        return width, height

    def _setup_3d():
        w, h = get_window_size()

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        try:
            gluPerspective(70, w / h, 0.1, 1000)
        except ZeroDivisionError:
            pass
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def _update_3d():
        _setup_3d()
        glViewport(0, 0, *get_window_size())

    # mainloop
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if not USING_RENDERDOC:
            _update_3d()
        glClearColor(0.5, 0.7, 1, 1.0)

        world.drawcall()
        renderer.render()

        glfw.poll_events()
        glfw.swap_buffers(window)

    try:
        glfw.terminate()
    except:
        error("PyCraft", "Failed to terminate glfw!")
        sys.exit("GLFW could not be terminated!")

    # end helpers
    try:
        # get all active child processes
        active = multiprocessing.active_children()

        for process in active:
            process.terminate()

        try:
            for child in active:
                child.kill()
        except:
            pass

    except:
        sys.exit("Helper processes could not be terminated. Please terminate them manually.")

    try:
        shutil.rmtree("cache/")
    except:
        sys.exit("Cache directory could not be deleted. Please delete it manually.")

    sys.exit("PyCraft has been terminated.")