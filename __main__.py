#################################################################
#  ______   __  __   ______   ______     __     ______   ______ *
# |  __  |  \ \/ /  |  ____| |  __  |   /__\   /  ____| |__  __|*
# | |__| |   \  /   | |      | |__| |  //__\\ | |__       |  |  *
# |  ____|    ||    | |      |______| / ____ \|  __|      |  |  *
# | |         ||    | |____  | |\ \  / /    \ | |         |  |  *
# |_|         ||    |______| |_| \_\/_/      \|_|         |__|  *
#################################################################

# Make this true to enter debug mode
test = False

# import all the modules
from logger import *
from load_shaders import *
from Classes import *
from pyglet.gl import *
from OpenGL.GL import *
import pyglet

# Warn if game is in debug mode
if test:
    warn('Main', "This is a test!")

# Use shaders function
def use_shader(shader_name="default"):
    # Link and use the shader program
    shaders[shader_name].use()
    log("main", f"Using shaders: {shader_name}:{shaders[shader_name]}")

# Load shaders
use_shaders = True
load_shaders()

if __name__ == '__main__':
    # shaders
    if use_shaders:
        use_shader()
    
    # Create window
    _window = window.Window(width=400, height=300, caption='PyCraft',
                    resizable=True)
    _window.set_visible()
    
    # initialize opengl
    # Background color
    glClearColor(0.5, 0.7, 1, 1)
    # Enable depth test
    glEnable(GL_DEPTH_TEST)
    # Enable backface culling
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    # Enable lighting
    glEnable(GL_LIGHTING)
    if not test:
        # Enable fog
        glEnable(GL_FOG)
        glFogfv(GL_FOG_COLOR, (GLfloat *
                int(_window.model.chunk_distance*16))(0.5, 0.69, 1.0, 10))
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogf(GL_FOG_START, _window.model.chunk_distance*3)
        glFogf(GL_FOG_END, _window.model.chunk_distance*4)
        # Texture blending
        glEnable (GL_LINE_SMOOTH)
        glEnable (GL_BLEND)
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glHint (GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
    
    # run the game
    pyglet.app.run()
