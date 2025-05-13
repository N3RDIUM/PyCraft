try:
    from pyglm import glm
except ImportError:
    import glm

from .state import State


class Camera:
    def __init__(self, state: State):
        self.fov: float = 45.0
        self.aspect: float = 16 / 9
        self.near: float = 0.1
        self.far: float = 1000.0

        self.state: State = state
        self.position: list[float] = [0.0, 0.0, 0.0]
        self.rotation: list[float] = [0.0, 0.0, 0.0]

        self.state.camera = self

    def get_matrix(self):
        matrix = glm.mat4(1.0)
        for i in range(3):
            thing = glm.vec3(0.0)
            thing[i] = 1.0
            matrix = glm.rotate(matrix, glm.radians(self.rotation[i]), thing)
        matrix = glm.translate(matrix, glm.vec3(self.position))

        width, height = self.state.window.size
        self.aspect = width / height

        return matrix, glm.perspective(self.fov, self.aspect, self.near, self.far)
