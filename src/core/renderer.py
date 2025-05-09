import glfw
import numpy as np
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_BACK,
    GL_COLOR_BUFFER_BIT,
    GL_CULL_FACE,
    GL_CW,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_CLAMP,
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

from .asset_manager import AssetManager
from .dynamic_vbo import DELETE_UNNEEDED, DynamicVBOHandler
from .shared_context import SharedContext
from .state import State
from .camera import Camera

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
        self.camera: Camera = Camera(state)

    def drawcall(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.15, 0.15, 0.15, 1.0)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CW)

        glEnable(GL_DEPTH_CLAMP)

        if self.state.player is not None:
            self.state.player.drawcall()

        if self.asset_manager is None:
            self.asset_manager = self.state.asset_manager
            return
        self.asset_manager.use_shader("main")

        matrix = self.camera.get_matrix()
        transform_loc = glGetUniformLocation(
            self.asset_manager.get_shader_program("main"), "transform"
        )
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, glm.value_ptr(matrix))

        for vbo in self.vbo_handler.all_buffers():
            buffer = vbo.latest_buffer

            if buffer is None:
                continue
            if not vbo.visible:
                continue

            glBindBuffer(GL_ARRAY_BUFFER, buffer)
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

            glDrawArrays(GL_TRIANGLES, 0, 16 * 16 * 16 * 36)

            glDisableVertexAttribArray(0)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

        self.vbo_handler.update(DELETE_UNNEEDED)

