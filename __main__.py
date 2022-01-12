#################################################################
#  ______   __  __   ______   ______     __     ______   ______ *
# |  __  |  \ \/ /  |  ____| |  __  |   /__\   /  ____| |__  __|*
# | |__| |   \  /   | |      | |__| |  //__\\ | |__       |  |  *
# |  ____|    ||    | |      |______| / ____ \|  __|      |  |  *
# | |         ||    | |____  | |\ \  / /    \ | |         |  |  *
# |_|         ||    |______| |_| \_\/_/      \|_|         |__|  *
#################################################################

# imports
import pyglet
import threading
from pyglet.gl import *

# inbuilt imports
import Classes as pycraft
from logger import *
from load_shaders import *
from helpers.terrain_generator_helper import *

info('main', 'Initializing PyCraft...')

# Load all the shaders
load_shaders()

def _update_world(world):
    world_gen_process = threading.Thread(target = start_generaion, args = ([world]), daemon = True)
    world_gen_process.start()

if __name__ == '__main__':
    # create window
    window = pycraft.PyCraftWindow(shader = shaders['default'], world_update_func = _update_world, width = 800, height = 500, resizable = True) 

    # Run the app
    info('main', 'Running PyCraft...')
    pyglet.app.run()