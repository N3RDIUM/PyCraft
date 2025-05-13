import os
from typing import Any

import numpy as np
from OpenGL.GL import (
    GL_FRAGMENT_SHADER,
    GL_LINEAR,
    GL_LINEAR_MIPMAP_LINEAR,
    GL_REPEAT,
    GL_RGB,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    GL_UNPACK_ALIGNMENT,
    GL_UNSIGNED_BYTE,
    GL_VERTEX_SHADER,
    glBindTexture,
    glGenerateMipmap,
    glGenTextures,
    glPixelStorei,
    glTexImage2D,
    glTexParameteri,
    glUseProgram,
)
from OpenGL.GL.shaders import compileProgram, compileShader, ShaderProgram
from PIL import Image

from .state import State

ASSET_DIR = "./assets/"


class AssetManager:
    def __init__(self, state: State) -> None:
        self.state: State = state
        self.state.asset_manager = self

        self.shaders: dict[str, ShaderProgram] = {}
        self.texture: np.uint32 | None = None

    def load_assets(self, asset_dir: str = ASSET_DIR, name_prefix: str = "") -> None:
        shader_dir = os.path.join(asset_dir, "shaders/")
        shader_pairs: set[str] = set()

        for file in os.listdir(shader_dir):
            name = file.split(".")[0]
            shader_pairs.add(name)

        for name in shader_pairs:
            with open(os.path.join(shader_dir, name + ".vert")) as f:
                vert: int = compileShader(f.read(), GL_VERTEX_SHADER)
            with open(os.path.join(shader_dir, name + ".frag")) as f:
                frag: int = compileShader(f.read(), GL_FRAGMENT_SHADER)
            program: ShaderProgram = compileProgram(vert, frag)
            self.shaders[name_prefix + name] = program

        texture_dir = os.path.join(asset_dir, "textures/")
        for file in os.listdir(texture_dir):
            texture = Image.open(os.path.join(texture_dir, file))
            data: np.typing.NDArray = np.array(texture.getdata())

            self.texture = glGenTextures(1)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glBindTexture(GL_TEXTURE_2D, self.texture)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(
                GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR
            )

            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGB,
                texture.size[0],
                texture.size[1],
                0,
                GL_RGB,
                GL_UNSIGNED_BYTE,
                data,
            )
            glGenerateMipmap(GL_TEXTURE_2D)

            glBindTexture(GL_TEXTURE_2D, 0)

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

    def bind_texture(self) -> None:
        if self.texture is None:
            return
        glBindTexture(GL_TEXTURE_2D, self.texture)
