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
        glClearColor(0.15, 0.15, 0.15, 1.0)

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

        matrix = self.camera.get_matrix()
        transform_loc = glGetUniformLocation(
            self.asset_manager.get_shader_program("main"), "transform"
        )
        glUniformMatrix4fv(transform_loc, 1, GL_FALSE, glm.value_ptr(matrix))

        self.asset_manager.bind_texture()
        self.mesh_handler.drawcall()
        self.mesh_handler.update(DELETE_UNNEEDED)

