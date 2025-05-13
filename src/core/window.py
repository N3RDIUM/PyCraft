import glfw
from OpenGL.GL import GL_TRUE, glViewport

from terrain.world import World

from .renderer import Renderer
from .state import State


class Window:
    def __init__(self) -> None:
        if not glfw.init():
            raise Exception(
                "[core.window.Window] Init failed: Could not initialize glfw"
            )

        glfw.window_hint(glfw.SAMPLES, 1)  # TODO Make configurable
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(640, 480, "Voxl", None, None)
        if not self.window:
            glfw.terminate()
            raise Exception(
                "[core.window.Window] Init failed: Could not create GLFW window"
            )
        glfw.make_context_current(self.window)

        self.state: State = State(self)
        self.renderer: Renderer = Renderer(self.state)
        self.world: World = World(self.state)

    def start_mainloop(self) -> None:
        while not glfw.window_should_close(self.window):
            width, height = self.size
            glViewport(0, 0, width, height)

            self.mainloop_step()

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        self.state.on_close()
        while self.state.shared_context_alive:
            pass
        glfw.terminate()

    def mainloop_step(self) -> None:
        self.renderer.drawcall()
        self.state.on_drawcall()

    @property
    def size(self) -> tuple[int, int]:
        return glfw.get_window_size(self.window)
