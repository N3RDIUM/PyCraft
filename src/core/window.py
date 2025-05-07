import glfw
from OpenGL.GL import GL_TRUE, glViewport

from .state import State
from .renderer import Renderer

class Window:
    def __init__(self) -> None:
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
        glfw.make_context_current(window)

        self.state: State = State(window)
        self.renderer: Renderer = Renderer(self.state)

    def start_mainloop(self) -> None:
        while not glfw.window_should_close(self.state.window):
            width, height = glfw.get_window_size(self.state.window)
            glViewport(0, 0, width, height)

            self.mainloop_step()

            glfw.swap_buffers(self.state.window)
            glfw.poll_events()

        self.state.on_close()
        while self.state.shared_context_alive:
            pass
        glfw.terminate()

    def mainloop_step(self) -> None:
        self.renderer.drawcall()
        self.state.on_drawcall()

