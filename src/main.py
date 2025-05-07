import math

import glfw
import numpy as np
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

from core.dynamic_vbo import DynamicVBO
from core.state import State

# TODO: use glm
# TODO: logging
# TODO: organize and refactor code
# TODO: update viewport on resize

data = np.random.rand(120).astype(np.float32)

VERTEX_SHADER = """
#version 330 core
layout(location = 0) in vec3 position;
uniform mat4 transform;
void main() {
    gl_Position = transform * vec4(position, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(1.0, 1.0, 1.0, 1.0);
}
"""


def main():
    if not glfw.init():
        raise Exception("[Main] GLFW could not be initialized")

    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(640, 480, "Hello World", None, None)
    if not window:
        glfw.terminate()
        raise Exception("[Main] Could not create GLFW window")

    glfw.make_context_current(window)
    state = State(window)
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = DynamicVBO(state)
    vbo.set_data(data)
    buffer = vbo.get_latest_buffer()
    if buffer is None:
        raise Exception("[Main] Failed to initialize DynamicVBO")

    shader_program = compileProgram(
        compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER),
    )

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.15, 0.15, 0.15, 1.0)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        glUseProgram(shader_program)

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

        transform_loc = glGetUniformLocation(shader_program, "transform")
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, rotation)

        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glDrawArrays(GL_TRIANGLES, 0, 120)

        glDisableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        state.on_drawcall()
        glfw.swap_buffers(window)
        glfw.poll_events()

    state.on_close()
    glfw.terminate()


if __name__ == "__main__":
    main()
