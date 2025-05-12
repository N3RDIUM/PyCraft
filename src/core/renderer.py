import numpy as np
from OpenGL.GL import *

try:
    from pyglm import glm
except ImportError:
    import glm

from .asset_manager import AssetManager
from .mesh import DELETE_UNNEEDED, MeshHandler
from .shared_context import SharedContext
from .state import State
from .camera import Camera
from terrain.world import RENDER_DIST
from terrain.chunk import CHUNK_SIDE

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

    def drawcall(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*(0.15 for _ in range(3)), 1.0)

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

        model = glm.mat4(1.0)
        projection, view = self.camera.get_matrix()
        camera = (
            -self.camera.position[0],
            -self.camera.position[1],
            -self.camera.position[2],
        )
        model_pos = glGetUniformLocation(
            self.asset_manager.get_shader_program("main"), "model"
        )
        view_pos = glGetUniformLocation(
            self.asset_manager.get_shader_program("main"), "view"
        )
        projection_pos = glGetUniformLocation(
            self.asset_manager.get_shader_program("main"), "projection"
        )
        glUniformMatrix4fv(model_pos, 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(view_pos, 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(projection_pos, 1, GL_FALSE, glm.value_ptr(projection))
        glUniform3f(glGetUniformLocation(self.asset_manager.get_shader_program("main"), "fogColor"), *(0.15 for _ in range(3)))
        glUniform1f(glGetUniformLocation(self.asset_manager.get_shader_program("main"), "fogStart"), 0.01)
        glUniform1f(glGetUniformLocation(self.asset_manager.get_shader_program("main"), "fogEnd"), CHUNK_SIDE * (RENDER_DIST - 1.25))
        glUniform3f(glGetUniformLocation(self.asset_manager.get_shader_program("main"), "camera"), *camera)

        self.asset_manager.bind_texture()
        self.mesh_handler.drawcall()
        self.mesh_handler.update(DELETE_UNNEEDED)

