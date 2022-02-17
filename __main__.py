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

if not glfw.init():
    raise Exception("glfw can not be initialized")

context = glfw.create_window(800, 500, "PyCraft", None, None)
glfw.make_context_current(context)

# mainloop
while not glfw.window_should_close(context):
    glfw.poll_events()
    glfw.swap_buffers(context)

    glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.13, 0.2, 0.3, 1.0)

glfw.terminate()
