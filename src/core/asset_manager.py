import os
from typing import Any

from OpenGL.GL import GL_FRAGMENT_SHADER, GL_VERTEX_SHADER, glUseProgram
from OpenGL.GL.shaders import compileProgram, compileShader

from .state import State

ASSET_DIR = "./assets/"


class AssetManager:
    def __init__(self, state: State) -> None:
        self.state: State = state
        self.state.asset_manager = self

        self.shaders = {}

    def load_assets(self, asset_dir: str = ASSET_DIR, name_prefix: str = "") -> None:
        shader_dir = os.path.join(asset_dir, "shaders/")
        shader_pairs = set()

        for file in os.listdir(shader_dir):
            name = file.split(".")[0]
            shader_pairs.add(name)

        for name in shader_pairs:
            with open(os.path.join(shader_dir, name + ".vert")) as f:
                vert = f.read()
            with open(os.path.join(shader_dir, name + ".frag")) as f:
                frag = f.read()
            self.shaders[name_prefix + name] = compileProgram(
                compileShader(vert, GL_VERTEX_SHADER),
                compileShader(frag, GL_FRAGMENT_SHADER),
            )

    def use_shader(self, name: str) -> None:
        if name not in self.shaders:
            raise Exception(
                f"[core.asset_manager.AssetManager] Tried to use shader {name} but it doesn't exist or isn't loaded yet"
            )
        glUseProgram(self.shaders[name])

    def get_shader_program(self, name: str) -> Any | None:
        if name not in self.shaders:
            raise Exception(
                f"[core.asset_manager.AssetManager] Tried to use shader {name} but it doesn't exist or isn't loaded yet"
            )
        return self.shaders[name]
