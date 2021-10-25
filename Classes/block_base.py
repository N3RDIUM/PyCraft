import pyglet
from pyglet.gl import *
import logging
blocks_all = {}
import os
import time
logging.basicConfig(level=logging.DEBUG)

def log(source, message):
    now = time.strftime("%H:%M:%S")
    logging.debug(f"({now}) [{source}]: {message}")

def load_texture(filename):
    log("Texture Loader", "Loading texture: " + filename)
    tex = pyglet.image.load(filename).get_texture()
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    return pyglet.graphics.TextureGroup(tex)

class BlockBase:
    def __init__(self, block_data, parent):
        self.block_data = {
            "block_textures": None,
            "block_pos": block_data["block_pos"],
            "block_faces": {
                "top": None,
                "bottom": None,
                "front": None,
                "back": None,
                "left": None,
                "right": None
            },
            "block_redstone_activated": False,
            "block_conducts_redstone": False,
            "parent": parent
        }
        self.chunk = parent

    def add_to_batch_and_save(self):
        x = self.block_data['block_pos']['x']
        y = self.block_data['block_pos']['y']
        z = self.block_data['block_pos']['z']
        X, Y, Z = x+1, y+1, z+1
        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))
        self.block_data['top'] = self.chunk.batch.add(4, GL_QUADS, self.block_data['block_textures']['top'],    ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), tex_coords)
        self.block_data['bottom'] = self.chunk.batch.add(4, GL_QUADS, self.block_data['block_textures']['bottom'], ('v3f', (x, y, z,  X, y, z,  X, y, Z,  x, y, Z)), tex_coords)
        self.block_data['front'] = self.chunk.batch.add(4, GL_QUADS, self.block_data['block_textures']['front'],  ('v3f', (x, y, z,  X, y, z,  X, Y, z,  x, Y, z)), tex_coords)
        self.block_data['back'] = self.chunk.batch.add(4, GL_QUADS, self.block_data['block_textures']['back'],   ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), tex_coords)
        self.block_data['left'] = self.chunk.batch.add(4, GL_QUADS, self.block_data['block_textures']['left'],   ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), tex_coords)
        self.block_data['right'] = self.chunk.batch.add(4, GL_QUADS, self.block_data['block_textures']['right'],  ('v3f', (X, y, z,  X, y, Z,  X, Y, Z,  X, Y, z)), tex_coords)

textures = {}

def get_all_textures(dir):
    for i in os.listdir(dir):
        if i.endswith(".png"):
            log("Texture Loader", "Loading texture: " + i)
            textures[i.split(".")[0]] = load_texture(dir+"/"+i)

get_all_textures("assets/textures/block/")

class grass_block(BlockBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.block_data["block_textures"] = {
            "top": textures["grass_block_top"],
            "left": textures["grass_block_side"],
            "right": textures["grass_block_side"],
            "front": textures["grass_block_side"],
            "back": textures["grass_block_side"],
            "bottom": textures["dirt"]
        }

blocks_all["grass"] = grass_block
