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

from terrain.block import BOX

from .asset_manager import AssetManager
from .dynamic_vbo import DELETE_UNNEEDED, DynamicVBOHandler
from .shared_context import SharedContext
from .state import State

fov = glm.radians(45.0)
aspect_ratio = 800 / 600
near = 0.1
far = 100.0 

def translate(box, pos):
    new = np.array(box, dtype=np.float32)
    for i in range(len(box)):
        f = i % 3
        new[i] += pos[f]
    return new

def gen_data():
    thing = []
    a = 16
    for x in range(-a, a + 1):
        for y in range(-a, a + 1):
            z = 0
            if (x + y)% 2 == 0:
                z = 1
            thing.append(translate(BOX, [x, y, z]))
    return np.vstack(tuple(thing))

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
        glEnable(GL_DEPTH_CLAMP)

        self.vbo.set_data(gen_data())

        if self.asset_manager is None:
            self.asset_manager = self.state.asset_manager
            return
        self.asset_manager.use_shader("main")

        width, height = self.state.window.size
        aspect_ratio = width / height

        model = glm.mat4(1.0)
        model = glm.translate(model, glm.vec3(0, 0, -64))
        model = glm.rotate(model, glm.radians(glfw.get_time() * 42), glm.vec3(0, 1, 0))

        camera = glm.mat4(1.0)
        camera = glm.rotate(camera, glm.radians(glfw.get_time() * 64), glm.vec3(0, 0, 1))

        matrix = glm.perspective(fov, aspect_ratio, near, far) * camera * model

        transform_loc = glGetUniformLocation(
            self.asset_manager.get_shader_program("main"), "transform"
        )
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, glm.value_ptr(matrix))

        buffer = self.vbo.latest_buffer
        if buffer is None:
            return

        glBindBuffer(GL_ARRAY_BUFFER, buffer)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glDrawArrays(GL_TRIANGLES, 0, 36 * 64 * 64)

        glDisableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # TODO: "DynamicVBOManager" to handle this and the set_data thing in the shared ctx thread
        self.vbo.update_buffers(mode=DELETE_UNNEEDED)
