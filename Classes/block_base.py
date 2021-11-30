# imports
import tqdm
import os
import pyglet
from pyglet.gl import *
from logger import *

# all the block types
blocks_all = {}

# Function to load a texture
def load_texture(filename):
    """
    load_texture

    * Loads a texture from a file

    :filename: path of the file to load
    """
    try:
        tex = pyglet.image.load(filename).get_texture()
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return pyglet.graphics.TextureGroup(tex)
    except:
        warn("Texture Loader", "Failed to load texture: " + filename)
        return None


class BlockBase:
    def __init__(self, block_data, parent):
        """
        BlockBase

        * Base class for all blocks

        :block_data: data of the block
        :parent: parent chunk
        """
        self.block_data = {
            "block_textures": None,
            "block_pos": block_data["block_pos"],
            "block_redstone_activated": False,
            "block_conducts_redstone": False,
            "parent": parent,
            "top": None,
            "bottom": None,
            "left": None,
            "right": None,
            "front": None,
            "back": None,
            "block_textures":{
                "top": None,
                "bottom": None,
                "left": None,
                "right": None,
                "front": None,
                "back": None
            }
        }
        self.chunk = parent
        self.generated = False

    def add_to_batch_and_save(self, *args, **kwargs):
        """
        add_to_batch_and_save

        * Adds the block to the batch and saves it to the block list
        """
        x = self.block_data['block_pos']['x']
        y = self.block_data['block_pos']['y']
        z = self.block_data['block_pos']['z']
        X, Y, Z = x+1, y+1, z+1
        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))

        if not self.chunk.parent.block_exists((x, y+1, z)):
            self.block_data['top'] = self.chunk.batch.add(
                4, GL_QUADS, self.block_data['block_textures']['top'],    ('v3f', (x, Y, Z,  X, Y, Z,  X, Y, z,  x, Y, z)), tex_coords)

        if not self.chunk.parent.block_exists((x, y-1, z)):
            self.block_data['bottom'] = self.chunk.batch.add(
                4, GL_QUADS, self.block_data['block_textures']['bottom'], ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z)), tex_coords)

        if not self.chunk.parent.block_exists((x-1, y, z)):
            self.block_data['left'] = self.chunk.batch.add(
                4, GL_QUADS, self.block_data['block_textures']['left'],   ('v3f', (x, y, z,  x, y, Z,  x, Y, Z,  x, Y, z)), tex_coords)

        if not self.chunk.parent.block_exists((x+1, y, z)):
            self.block_data['right'] = self.chunk.batch.add(
                4, GL_QUADS, self.block_data['block_textures']['right'],  ('v3f', (X, y, Z,  X, y, z,  X, Y, z,  X, Y, Z)), tex_coords)

        if not self.chunk.parent.block_exists((x, y, z+1)):
            self.block_data['front'] = self.chunk.batch.add(
                4, GL_QUADS, self.block_data['block_textures']['front'],  ('v3f', (x, y, Z,  X, y, Z,  X, Y, Z,  x, Y, Z)), tex_coords)

        if not self.chunk.parent.block_exists((x, y, z-1)):
            self.block_data['back'] = self.chunk.batch.add(
                4, GL_QUADS, self.block_data['block_textures']['back'],   ('v3f', (X, y, z,  x, y, z,  x, Y, z,  X, Y, z)), tex_coords)

        self.generated = True

    def remove(self, *args, **kwargs):
        """
        remove

        * Removes the block from the batch
        """
        if self.generated:
            try:
                self.block_data['top'].delete()
            except:
                pass
            try:
                self.block_data['bottom'].delete()
            except:
                pass
            try:
                self.block_data['left'].delete()
            except:
                pass
            try:
                self.block_data['right'].delete()
            except:
                pass
            try:
                self.block_data['front'].delete()
            except:
                pass
            try:
                self.block_data['back'].delete()
            except:
                pass
            self.generated = False

textures = {}


def get_all_textures(dir):
    """
    get_all_textures

    * Gets all the textures in a directory

    :dir: directory to look in
    """
    log("Texture Loader", "Loading textures...")
    for i in tqdm.tqdm(os.listdir(dir)):
        if i.endswith(".png"):
            #log("Texture Loader", "Loading texture: " + i)
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


class iron_ore(BlockBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.block_data["block_textures"] = {
            "top": textures["stone"],
            "left": textures["iron_ore"],
            "right": textures["iron_ore"],
            "front": textures["iron_ore"],
            "back": textures["iron_ore"],
            "bottom": textures["stone"]
        }


blocks_all["iron_ore"] = iron_ore


class gold_ore(BlockBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.block_data["block_textures"] = {
            "top": textures["stone"],
            "left": textures["gold_ore"],
            "right": textures["gold_ore"],
            "front": textures["gold_ore"],
            "back": textures["gold_ore"],
            "bottom": textures["stone"]
        }


blocks_all["gold_ore"] = gold_ore
