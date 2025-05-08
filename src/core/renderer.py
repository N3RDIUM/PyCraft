import glfw
import numpy as np
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_BACK,
    GL_COLOR_BUFFER_BIT,
    GL_CULL_FACE,
    GL_CW,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_FALSE,
    GL_FLOAT,
    GL_LESS,
    GL_TRIANGLES,
    glBindBuffer,
    glBindVertexArray,
    glClear,
    glClearColor,
    glCullFace,
    glDepthFunc,
    glDisableVertexAttribArray,
    glDrawArrays,
    glEnable,
    glEnableVertexAttribArray,
    glFrontFace,
    glGenVertexArrays,
    glGetUniformLocation,
    glUniformMatrix4fv,
    glVertexAttribPointer,
)

try:
    from pyglm import glm
except ImportError:
    import glm

from terrain.block import BOX

from .asset_manager import AssetManager
from .dynamic_vbo import DELETE_UNNEEDED, DynamicVBOHandler
from .shared_context import SharedContext
from .state import State

def gen_data():
    blocks = []
    for i in range(16):
        for j in range(16):
            blocks.append(BOX)
    return np.vstack(tuple(blocks))

class Renderer:
    def __init__(self, state: State) -> None:
        self.state = state
        self.window = state.window
        self.shared: SharedContext = SharedContext(state)

        self.vao: np.uint32 = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.shared.start_thread()

        self.asset_manager: AssetManager | None = None

        self.vbo_handler = DynamicVBOHandler(state)
        self.vbo = self.vbo_handler.new_buffer("main")
        self.shared.register_vbo_handler(self.vbo_handler, "main")

    def drawcall(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.15, 0.15, 0.15, 1.0)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CW)

        self.vbo.set_data(gen_data())

        if self.asset_manager is None:
            self.asset_manager = self.state.asset_manager
            return
        self.asset_manager.use_shader("main")

        angle: float = glm.radians(glfw.get_time() * 64)
        matrix = glm.mat4()
        matrix = glm.translate(matrix, glm.vec3(0, 0, 64))
        matrix = glm.rotate(matrix, angle, glm.vec3(1, 0, 1))

        transform_loc = glGetUniformLocation(
            self.asset_manager.get_shader_program("main"), "transform"
        )
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, glm.value_ptr(rotation))

        buffer = self.vbo.latest_buffer
        if buffer is None:
            return

        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glDrawArrays(GL_TRIANGLES, 0, 36 * 16 * 16)

        glDisableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # TODO: "DynamicVBOManager" to handle this and the set_data thing in the shared ctx thread
        self.vbo.update_buffers(mode=DELETE_UNNEEDED)
