import glfw
from OpenGL.GL import GL_TRUE

from .state import State

class Window:
    def __init__(self):
        if not glfw.init():
            raise Exception("[core.window.Window] Init failed: Could not initialize glfw")

        glfw.window_hint(glfw.SAMPLES, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        window = glfw.create_window(640, 480, "PyCraft", None, None)
        if not window:
            glfw.terminate()
            raise Exception("[core.window.Window] Init failed: Could not create GLFW window")

        self.state: State = State(window)

    def mainloop(self):
        pass

