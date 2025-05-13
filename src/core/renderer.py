import numpy as np
from OpenGL.GL import (
    GL_BACK,
    GL_CCW,
    GL_COLOR_BUFFER_BIT,
    GL_CULL_FACE,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_CLAMP,
    GL_DEPTH_TEST,
    GL_FALSE,
    GL_LESS,
    glBindVertexArray,
    glClear,
    glClearColor,
    glCullFace,
    glDepthFunc,
    glEnable,
    glFrontFace,
    glGenVertexArrays,
    glGetUniformLocation,
    glUniform1f,
    glUniform3f,
    glUniformMatrix4fv,
)

try:
    from pyglm import glm
except ImportError:
    import glm

from terrain.chunk import CHUNK_SIDE
from terrain.world import RENDER_DIST

from .asset_manager import AssetManager
from .camera import Camera
from .mesh import DELETE_UNNEEDED, MeshHandler
from .shared_context import SharedContext
from .state import State

BACKGROUND = (0.15 for _ in range(3))


class Renderer:
    def __init__(self, state: State) -> None:
        self.state = state
        self.window = state.window
        self.shared: SharedContext = SharedContext(state)

        self.vao: np.uint32 = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.shared.start_thread()

        self.asset_manager: AssetManager | None = None

        self.mesh_handler = MeshHandler(state)
        self.camera: Camera = Camera(state)

    def set_uniforms(self) -> None:
        model = glm.mat4(1.0)
        view, projection = self.camera.get_matrix()
        camera = (
            -self.camera.position[0],
            -self.camera.position[1],
            -self.camera.position[2],
        )
        fog_start = 0.1
        fog_end = CHUNK_SIDE * (RENDER_DIST - 1.25)

        shader = self.asset_manager.get_shader_program("main")

        model_pos = glGetUniformLocation(shader, "model")
        view_pos = glGetUniformLocation(shader, "view")
        projection_pos = glGetUniformLocation(shader, "projection")
        fogColor_pos = glGetUniformLocation(shader, "fogColor")
        fogStart_pos = glGetUniformLocation(shader, "fogStart")
        fogEnd_pos = glGetUniformLocation(shader, "fogEnd")
        camera_pos = glGetUniformLocation(shader, "camera")

        glUniformMatrix4fv(model_pos, 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(view_pos, 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(projection_pos, 1, GL_FALSE, glm.value_ptr(projection))
        glUniform3f(fogColor_pos, *BACKGROUND)
        glUniform1f(fogStart_pos, fog_start)
        glUniform1f(fogEnd_pos, fog_end)
        glUniform3f(camera_pos, *camera)

    def drawcall(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*BACKGROUND, 1.0)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)

        glEnable(GL_DEPTH_CLAMP)

        if self.state.player is not None:
            self.state.player.drawcall()

        if self.asset_manager is None:
            self.asset_manager = self.state.asset_manager
            return
        self.asset_manager.use_shader("main")

        self.set_uniforms()

        self.asset_manager.bind_texture()
        self.mesh_handler.drawcall()
        self.mesh_handler.update(DELETE_UNNEEDED)
