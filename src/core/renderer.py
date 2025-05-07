from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_FALSE,
    GL_FLOAT,
    GL_FRAGMENT_SHADER,
    GL_LESS,
    GL_TRIANGLES,
    GL_TRUE,
    GL_VERTEX_SHADER,
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
    glUseProgram,
    glVertexAttribPointer,
)
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

from .state import State
from .shared_context import SharedContext

class Renderer:
    def __init__(self, state: State) -> None:
        self.state = state
        self.window = state.window
        self.shared: SharedContext = SharedContext(state)

        self.vao: np.uint32 = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.shared.start_thread()

        # TODO: Shader manager

    def drawcall(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.15, 0.15, 0.15, 1.0)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        # TODO: Use shader program here
        # TODO: Render here

