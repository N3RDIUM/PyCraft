from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_COLOR_BUFFER_BIT,
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
    glDepthFunc,
    glDisableVertexAttribArray,
    glDrawArrays,
    glEnable,
    glEnableVertexAttribArray,
    glGenVertexArrays,
    glGetUniformLocation,
    glUniformMatrix4fv,
    glVertexAttribPointer,
)
import numpy as np
import glfw
import math

from .dynamic_vbo import DynamicVBO
from .state import State
from .asset_manager import AssetManager
from .shared_context import SharedContext

class Renderer:
    def __init__(self, state: State) -> None:
        self.state = state
        self.window = state.window
        self.shared: SharedContext = SharedContext(state)

        self.vao: np.uint32 = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.shared.start_thread()

        self.asset_manager: AssetManager | None = None

        self.vbo = DynamicVBO(state)
        self.vbo.set_data(np.random.rand(120).astype(np.float32))

    def drawcall(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.15, 0.15, 0.15, 1.0)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        if self.asset_manager is None:
            self.asset_manager = self.state.asset_manager
        self.asset_manager.use_shader("main")

        angle: float = glfw.get_time()

        cos_theta = math.cos(angle)
        sin_theta = math.sin(angle)

        rotation = np.array(
            [
                [cos_theta, -sin_theta, 0, 0],
                [sin_theta, cos_theta, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ],
            dtype=np.float32,
        )

        transform_loc = glGetUniformLocation(self.asset_manager.get_shader_program("main"), "transform")
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, rotation)

        buffer = self.vbo.latest_buffer

        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glDrawArrays(GL_TRIANGLES, 0, 40)

        glDisableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

