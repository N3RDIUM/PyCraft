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
import sys

# internal imports
from core.renderer import *
from player import *
from settings import *
from terrain.world import *
from core.text import text

# start helpers
try:
    shutil.rmtree("cache/")
except FileNotFoundError:
    pass

if DEV_MODE:
    warn("PyCraft", "DEV_MODE is enabled. Please don't use this in production.")
if DISABLE_CHUNK_CULLING:
    warn("PyCraft", "DISABLE_CHUNK_CULLING is enabled. This may cause significant FPS drops.")

chunk_generators = []
chunk_builders = []

for i in range(CHUNK_GENERATORS):
    chunk_generator = subprocess.Popen(
        [sys.executable, "helpers/chunk_generator.py"])
    chunk_generators.append(chunk_generator)

for i in range(CHUNK_BUILDERS):
    chunk_builder = subprocess.Popen(
        [sys.executable, "helpers/chunk_builder.py"])
    chunk_builders.append(chunk_builder)

flask_process = subprocess.Popen(
        [sys.executable, "helpers/flask_server.py"])

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
    if not DEV_MODE and not USING_GRAPHICS_DEBUGGER:
        glEnable(GL_FOG)
        glFogfv(GL_FOG_COLOR, (GLfloat * int(32))(0.5, 0.69, 1.0, 10))
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogf(GL_FOG_START, CHUNK_SIZE//4)
        distance = world.render_distance
        glFogf(GL_FOG_END, (world.render_distance + 2)/4 * CHUNK_SIZE + 1)

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
        if not USING_GRAPHICS_DEBUGGER:
            _update_3d()
        glClearColor(0.5, 0.7, 1, 1.0)

        world.drawcall()
        renderer.render()
        
        _fps = world.fpss
        fps = 0
        for value in _fps:
            fps += value
        fps /= len(_fps)

        text(10, 10, "FPS            : " + str(int(fps)))
        text(10, 32, "Position       : " + str([int(world.player.pos[0]), int(world.player.pos[1]), int(world.player.pos[2])]))
        text(10, 54, "Chunks         : " + str(len(world.chunks)))
        text(10, 76, "Render Distance: " + str(world.render_distance))

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

        for process in active:
            process.join()

        for process in active:
            process.close()
    except:
        sys.exit(
            "Helper processes could not be terminated. Please terminate them manually.")

    try:
        shutil.rmtree("cache/")
    except:
        sys.exit("Cache directory could not be deleted. Please delete it manually.")

    sys.exit("PyCraft has been terminated.")
