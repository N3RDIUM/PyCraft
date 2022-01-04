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
from pyglet.gl import *

# inbuilt imports
import Classes as pycraft
from logger import *
from load_shaders import *

info('main', 'Initializing PyCraft...')

# Load all the shaders
load_shaders()

if __name__ == '__main__':
    # create window
    window = pycraft.PyCraftWindow(shader = shaders['default'], width = 800, height = 500, resizable = True)
    
    # Run the app
    info('main', 'Running PyCraft...')
    pyglet.app.run()

info('main', 'Stopping!')
