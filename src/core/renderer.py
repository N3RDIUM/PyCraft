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
try:
    from pyglm import glm
except ImportError:
    import glm

from .dynamic_vbo import DynamicVBOHandler, DELETE_UNNEEDED
from .state import State
from .asset_manager import AssetManager
from .shared_context import SharedContext

def gen_data():
    data = np.random.rand(1200).astype(np.float32)
    data *= 2
    data -= 1
    data /= 2
    return data

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

        if self.asset_manager is None:
            self.asset_manager = self.state.asset_manager
            return
        self.asset_manager.use_shader("main")
        self.vbo.set_data(gen_data())

        angle: float = glm.radians(glfw.get_time() * 10)
        matrix = glm.mat4()
        rotation = glm.rotate(matrix, angle, glm.vec3(0, 1, 0))

        transform_loc = glGetUniformLocation(self.asset_manager.get_shader_program("main"), "transform")
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, glm.value_ptr(rotation))
    
        buffer = self.vbo.latest_buffer
        if buffer is None:
            return

        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glDrawArrays(GL_TRIANGLES, 0, 400)

        glDisableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # TODO: "DynamicVBOManager" to handle this and the set_data thing in the shared ctx thread
        self.vbo.update_buffers(mode = DELETE_UNNEEDED)

