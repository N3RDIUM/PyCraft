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
        self.block_data['top'] = self.chunk.batch.add(4, GL_QUADS, self.block_data['block_textures']['top'],    ('v3f', (x, Y,Z,  X, Y, Z,  X, Y, z,  x, Y, z)), tex_coords)
        self.block_data['bottom'] = self.chunk.batch.add(4, GL_QUADS, self.block_data['block_textures']['bottom'], ('v3f', (X, y,Z,  X, y, z,  X, Y, z,  X, Y, Z)), tex_coords)
        self.block_data['front'] = self.chunk.batch.add(4, GL_QUADS, self.block_data['block_textures']['front'],  ('v3f', (x, y,Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), tex_coords)
        self.block_data['back'] = self.chunk.batch.add(4, GL_QUADS, self.block_data['block_textures']['back'],   ('v3f', (X, y,z,  x, y, z,  x, Y, z,  X, Y, z)), tex_coords)
        self.block_data['left'] = self.chunk.batch.add(4, GL_QUADS, self.block_data['block_textures']['left'],   ('v3f',(x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), tex_coords)
        self.block_data['right'] = self.chunk.batch.add(4, GL_QUADS, self.block_data['block_textures']['right'],  ('v3f', (X, y,Z,  X, y, z,  X, Y, z,  X, Y, Z)), tex_coords)

textures = {}

def get_all_textures(dir):
    for i in os.listdir(dir):
        if i.endswith(".png"):
            log("Texture Loader", "Loading texture: " + i)
            textures[i.split(".")[0]] = load_texture(dir+"/"+i)

get_all_textures("assets/textures/block/")

class grass(BlockBase):
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

blocks_all["grass"] = grass

class dirt(BlockBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.block_data["block_textures"] = {
            "top": textures["dirt"],
            "left": textures["dirt"],
            "right": textures["dirt"],
            "front": textures["dirt"],
            "back": textures["dirt"],
            "bottom": textures["dirt"]
        }

blocks_all["dirt"] = dirt

class stone(BlockBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.block_data["block_textures"] = {
            "top": textures["stone"],
            "left": textures["stone"],
            "right": textures["stone"],
            "front": textures["stone"],
            "back": textures["stone"],
            "bottom": textures["stone"]
        }

blocks_all["stone"] = stone

class cobblestone(BlockBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.block_data["block_textures"] = {
            "top": textures["cobblestone"],
            "left": textures["cobblestone"],
            "right": textures["cobblestone"],
            "front": textures["cobblestone"],
            "back": textures["cobblestone"],
            "bottom": textures["cobblestone"]
        }
    
blocks_all["cobblestone"] = cobblestone

class bedrock(BlockBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.block_data["block_textures"] = {
            "top": textures["bedrock"],
            "left": textures["bedrock"],
            "right": textures["bedrock"],
            "front": textures["bedrock"],
            "back": textures["bedrock"],
            "bottom": textures["bedrock"]
        }

blocks_all["bedrock"] = bedrock
